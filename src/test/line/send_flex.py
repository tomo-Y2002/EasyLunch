import sys
import os
from flask import Flask, request, abort
from linebot.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent
import json

# プロジェクトのルートディレクトリへのパスを追加
# これを追加しないと、src以下のモジュールをimportできない
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
)
from src.line.line import LineMessagingClient
from src.line.utils import create_carousel, get_id

app = Flask(__name__)
# defaultで"config.yaml"が設定されているので、指定しなくてもOK
line_bot_handler = LineMessagingClient(config_path="config.yaml")


@line_bot_handler.handler.add(MessageEvent, message=TextMessageContent)
def reply_FM(event):
    template = "./src/test/line/hotpepper.json"
    with open(template, "r", encoding="utf-8") as f:
        stores = json.load(f)
    template_path = "./src/line/template.json"
    userId = get_id(event)
    try:
        flex_message = create_carousel(userId, stores, template_path=template_path)
        line_bot_handler.send_flex(flex_message)
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
