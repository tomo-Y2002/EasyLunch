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
from src.db.access.utils import is_one_hour_passed
from src.db.access.visit import VisitDB
from src.llm.llm_call import LLM
from src.llm.prompt import select_prompt
from src.llm.utils import build_user_prompt_refine, build_user_prompt_extract
from src.api.google_logging import Logging
from src.api.google_places import GooglePlacesClient

if os.path.exists("config.yaml"):
    with open("config.yaml", encoding="utf-8") as f:
        config_data = yaml.safe_load(f)
        for key, value in config_data.items():
            os.environ[key] = str(value)

logger = Logging(is_gc=bool(os.environ.get("IS_GOOGLE_CLOUD") == "true"))

app = Flask(__name__)
line_bot_handler = LineMessagingClient(
    line_channel_secret=os.environ.get("LINE_CHANNEL_SECRET"),
    line_channel_access_token=os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"),
    port=os.environ.get("PORT"),
    is_gc=bool(os.environ.get("IS_GOOGLE_CLOUD") == "true"),
)
logger.log_text(f"LINE_CHANNEL_SECRET: {os.environ.get('LINE_CHANNEL_SECRET')}")
logger.log_text(
    f"LINE_CHANNEL_ACCESS_TOKEN: {os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')}"
)
logger.log_text(f"PORT: {os.environ.get('PORT')}")
logger.log_text(f"type(PORT): {type(os.environ.get('PORT'))}")
chat_db = ChatDB(
    host=os.environ.get("MYSQL_HOST"),
    user=os.environ.get("MYSQL_USER"),
    password=os.environ.get("MYSQL_PASSWORD"),
    database=os.environ.get("MYSQL_DATABASE"),
    is_gc=bool(os.environ.get("IS_GOOGLE_CLOUD") == "true"),
)
logger.log_text(f"MYSQL_HOST: {os.environ.get('MYSQL_HOST')}")
logger.log_text(f"MYSQL_USER: {os.environ.get('MYSQL_USER')}")
logger.log_text(f"MYSQL_PASSWORD: {os.environ.get('MYSQL_PASSWORD')}")
logger.log_text(f"MYSQL_DATABASE: {os.environ.get('MYSQL_DATABASE')}")
logger.log_text(f"IS_GOOGLE_CLOUD: {os.environ.get('IS_GOOGLE_CLOUD')}")
visit_db = VisitDB(
    host=os.environ.get("MYSQL_HOST"),
    user=os.environ.get("MYSQL_USER"),
    password=os.environ.get("MYSQL_PASSWORD"),
    database=os.environ.get("MYSQL_DATABASE"),
    is_gc=bool(os.environ.get("IS_GOOGLE_CLOUD") == "true"),
)
llm_client = LLM(
    llm_type=os.environ.get("LLM_TYPE"),
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    aws_region_name=os.environ.get("AWS_REGION"),
    azure_api_key=os.environ.get("AZURE_API_KEY"),
    azure_endpoint=os.environ.get("AZURE_ENDPOINT"),
    azure_api_version=os.environ.get("AZURE_API_VERSION"),
)
logger.log_text(f"LLM_TYPE: {os.environ.get('LLM_TYPE')}")
logger.log_text(f"AWS_ACCESS_KEY_ID: {os.environ.get('AWS_ACCESS_KEY_ID')}")
logger.log_text(f"AWS_SECRET_ACCESS_KEY: {os.environ.get('AWS_SECRET_ACCESS_KEY')}")
logger.log_text(f"AWS_REGION: {os.environ.get('AWS_REGION')}")
logger.log_text(f"AZURE_API_KEY: {os.environ.get('AZURE_API_KEY')}")
logger.log_text(f"AZURE_ENDPOINT: {os.environ.get('AZURE_ENDPOINT')}")
logger.log_text(f"AZURE_API_VERSION: {os.environ.get('AZURE_API_VERSION')}")

places_client = GooglePlacesClient(
    google_places_api_key=os.environ.get("GOOGLE_PLACES_API_KEY"),
)
logger.log_text(f"GOOGLE_PLACES_API_KEY: {os.environ.get('GOOGLE_PLACES_API_KEY')}")


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
    logger.log_text(f"ユーザ {user_id} がメッセージを送信しました: {text}")
    line_bot_handler.send_loading(user_id)
    # フィルタリング処理
    # to be implemented

    # 会話履歴DBから、該当のuser_idの会話履歴を取得
    conn = chat_db.connect()
    chat_history = chat_db.get(conn=conn, user_id=user_id)
    chat_db.close(conn)
    print("会話履歴DBとの接続を終了")
    logger.log_text("会話履歴DBとの接続を終了")

    # 最後の会話から一定時間経過していたら、該当のuser_idの会話履歴を削除
    if len(chat_history)>0 and is_one_hour_passed(last_access_time=chat_history[-1][-1]):
        conn = chat_db.connect()
        chat_db.erase(conn=conn,user_id=user_id)
        conn.commit()
        chat_db.close(conn)
        chat_history = []

    # 来店履歴DBから、該当のuser_idの来店履歴を取得
    conn = visit_db.connect()
    visit_history = visit_db.get(conn=conn, user_id=user_id)
    visit_db.close(conn)
    print("来店履歴の取得完了")
    logger.log_text("来店履歴の取得完了")

    prompt_extract_user = build_user_prompt_extract(
        request=text,
        chat=chat_history,
    )
    # print(f"prompt_extract_user: {prompt_extract_user}")
    prompt_extract = llm_client._build_prompt(
        prompt_system=select_prompt("extract_places"),
        image_encoded="",
        prompt_user=prompt_extract_user,
    )
    condition = llm_client.call_retry(mode="extract_places", prompt=prompt_extract)
    print("情報抽出完了")
    logger.log_text("情報抽出完了")

    # ホットペッパーAPIで飲食店検索

    query = json.loads(condition)["keyword"]
    stores = places_client.search_essential(query, count=5)
    print("Google Placesでの検索完了")
    logger.log_text("Google Placesでの検索完了")
    logger.log_text(f"検索結果: {stores}")

    # 来店履歴から、ユーザに沿ったものがあればLLMで抽出して返す
    stores_visited = []
    for info in visit_history:
        logger.log_text(f"来店履歴をAPIで検索開始: {info}")
        res = places_client.search_with_id(id=info[2])
        if len(res) != 0:
            stores_visited.append(res[0])
    stores_visited = stores_visited[:10]  # 10件までに制限
    print("来店履歴の検索完了")
    logger.log_text("来店履歴の検索完了")
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
        stores[-1] = places_client.search_with_id(id=id_selected)[0]  # 置換作業
    print("来店履歴からの情報追加完了")
    logger.log_text("来店履歴からの情報追加完了")

    # storesをFlex Messageに変換して、ユーザに返す
    if len(stores) == 0:
        line_bot_handler.send_text(user_id, "条件に合うお店が見つかりませんでした 😢")
        print("条件に合うお店が見つからなかったメッセージを送信")
        logger.log_text("条件に合うお店が見つからなかったメッセージを送信")
    else:
        flex_message = create_carousel(user_id, stores=stores, num=5)
        line_bot_handler.send_flex(flex_message)
        print("Flex Messageの送信完了")
        logger.log_text("Flex Messageの送信完了")

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
    logger.log_text("会話履歴の更新完了")


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
