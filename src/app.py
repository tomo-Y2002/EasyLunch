import sys
import os
import yaml
import json
from flask import Flask, request, abort
from linebot.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent, PostbackEvent


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.line.line import LineMessagingClient
from src.line.utils import create_carousel, get_id
from src.db.access.chat import ChatDB
from src.db.access.visit import VisitDB
from src.llm.llm_call import LLM
from src.llm.prompt import select_prompt
from src.llm.utils import build_user_prompt_refine
from src.api.hot_pepper import HotPepperClient

if os.path.exists("config.yaml"):
    with open("config.yaml", encoding="utf-8") as f:
        config_data = yaml.safe_load(f)
        for key, value in config_data.items():
            os.environ[key] = str(value)

app = Flask(__name__)
line_bot_handler = LineMessagingClient(
    line_channel_secret=os.environ.get("LINE_CHANNEL_SECRET"),
    line_channel_access_token=os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"),
    port=os.environ.get("PORT"),
)
chat_db = ChatDB(
    host=os.environ.get("MYSQL_HOST"),
    user=os.environ.get("MYSQL_USER"),
    password=os.environ.get("MYSQL_PASSWORD"),
    database=os.environ.get("MYSQL_DATABASE"),
)
visit_db = VisitDB(
    host=os.environ.get("MYSQL_HOST"),
    user=os.environ.get("MYSQL_USER"),
    password=os.environ.get("MYSQL_PASSWORD"),
    database=os.environ.get("MYSQL_DATABASE"),
)
llm_client = LLM(
    llm_type="claude 3.5 sonnet",
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    region_name=os.environ.get("AWS_REGION"),
)
hotpepper_client = HotPepperClient(
    hot_pepper_api_key=os.environ.get("HOT_PEPPER_API_KEY"),
    hot_pepper_lat=os.environ.get("HOT_PEPPER_LAT"),
    hot_pepper_lng=os.environ.get("HOT_PEPPER_LNG"),
    hot_pepper_range=os.environ.get("HOT_PEPPER_RANGE"),
)


@line_bot_handler.handler.add(PostbackEvent)
def on_postback(event):
    postback_data = event.postback.data
    user_id = get_id(event)

    if postback_data == "お問い合わせ":
        print(f"ユーザ {user_id} がお問い合わせを選択しました")
        # 会話履歴データベースをUserIDに関して初期化
        conn = chat_db.connect()
        chat_db.erase(conn=conn, user_id=user_id)
        chat_db.commit(conn)
        chat_db.close(conn)
    elif postback_data.startswith("店のid"):
        # 来店履歴データベースにUserIDと店舗IDを追加
        store_id = postback_data.split("店のid")[1]
        print(f"ユーザ {user_id} が店舗id {store_id}の店に行きました。")
        conn = visit_db.connect()
        visit_db.post(conn=conn, user_id=user_id, store_id=store_id)
        visit_db.commit(conn)
        visit_db.close(conn)


@line_bot_handler.handler.add(MessageEvent, message=TextMessageContent)
def on_reply(event):
    text = event.message.text
    user_id = get_id(event)
    print(f"ユーザ {user_id} がメッセージを送信しました: {text}")

    # フィルタリング処理
    # to be implemented

    # 会話履歴DBから、該当のuser_idの会話履歴を取得
    conn = chat_db.connect()
    chat_history = chat_db.get(conn=conn, user_id=user_id)
    chat_db.close(conn)
    print("会話履歴の取得完了")

    # 来店履歴DBから、該当のuser_idの来店履歴を取得
    conn = visit_db.connect()
    visit_history = visit_db.get(conn=conn, user_id=user_id)
    visit_db.close(conn)
    print("来店履歴の取得完了")

    # ユーザの要望から、ホットペッパーAPIに入れるための情報抽出
    prompt_extract = llm_client._build_prompt(
        prompt_system=select_prompt("extract"),
        image_encoded="",
        prompt_user=text,  # to be updated
    )
    condition = llm_client.call_retry(mode="extract", prompt=prompt_extract)
    print("情報抽出完了")

    # ホットペッパーAPIで飲食店検索
    condition = json.loads(condition)
    stores = hotpepper_client.search_essential(condition, count=15)
    print("ホットペッパーでの検索完了")

    # 来店履歴から、ユーザに沿ったものがあればLLMで抽出して返す
    stores_visited = []
    for info in visit_history:
        res = hotpepper_client.search_essential({"id": info[2]}, count=1)
        if len(res) != 0:
            stores_visited.append(res[0])
    stores_visited = stores_visited[:10]  # 10件までに制限
    print("来店履歴の検索完了")
    prompt_refine_user = build_user_prompt_refine(
        request=text,
        chat=chat_history,
        stores_visited=stores_visited,
    )
    prompt_refine = llm_client._build_prompt(
        prompt_system=select_prompt("refine"),
        image_encoded="",
        prompt_user=prompt_refine_user,
    )
    res_refine = llm_client.call_retry(mode="refine", prompt=prompt_refine)
    id_selected = json.loads(res_refine)["id"]
    shop_ids_in_stores = [store["id"] for store in stores]
    if id_selected != "" and id_selected not in shop_ids_in_stores:
        stores[-1] = hotpepper_client.search_essential({"id": id_selected}, count=1)[
            0
        ]  # 置換作業
    print("来店履歴からの情報追加完了")

    # storesをFlex Messageに変換して、ユーザに返す
    if len(stores) == 0:
        line_bot_handler.send_text(user_id, "条件に合うお店が見つかりませんでした 😢")
        print("条件に合うお店が見つからなかったメッセージを送信")
    else:
        flex_message = create_carousel(user_id, stores=stores, num=5)
        line_bot_handler.send_flex(flex_message)
        print("Flex Messageの送信完了")

    # 会話履歴DBにユーザとBOTの返答を追加
    conn = chat_db.connect()
    chat_db.post(
        conn=conn,
        user_id=user_id,
        speaker="USER",
        message=text,
    )
    chat_db.post(
        conn=conn,
        user_id=user_id,
        speaker="BOT",
        message=json.dumps(stores, ensure_ascii=False, indent=2),
    )
    chat_db.commit(conn)
    chat_db.close(conn)
    print("会話履歴の更新完了")


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        line_bot_handler.handle_webhook(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=line_bot_handler.port, debug=False)
