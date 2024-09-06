import sys
import os
from flask import Flask, request, abort
from linebot.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent
import yaml

# プロジェクトのルートディレクトリへのパスを追加
# これを追加しないと、src以下のモジュールをimportできない
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
)
from src.line.line import LineMessagingClient
from src.line.utils import get_id

app = Flask(__name__)
with open("config.yaml", encoding="utf-8") as f:
    configs = yaml.safe_load(f)

line_bot_handler = LineMessagingClient(
    line_channel_secret=configs["LINE_CHANNEL_SECRET"],
    line_channel_access_token=configs["LINE_CHANNEL_ACCESS_TOKEN"],
    port=configs["PORT"],
)


# メッセージ受信時にuserIdを返信する
@line_bot_handler.handler.add(MessageEvent, message=TextMessageContent)
def reply_received(event):
    user_id = get_id(event)
    msg = "あなたのuserIdは" + user_id + "です"
    try:
        line_bot_handler.send_text(user_id, msg)
    except Exception as e:
        print(f"メッセージ送信エラー: {e}")


# @app.routeはclass上に記述することはできず、別のファイルに記述することも煩雑なため、main関数と同じファイル内に記述する
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
