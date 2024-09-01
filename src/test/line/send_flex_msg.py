import sys
import os
from flask import Flask, request, abort
from linebot.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent

# プロジェクトのルートディレクトリへのパスを追加
# これを追加しないと、src以下のモジュールをimportできない
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
)
from src.line.line import LineMessagingApi

app = Flask(__name__)
# defaultで"config.yaml"が設定されているので、指定しなくてもOK
line_bot_handler = LineMessagingApi(config_path="config.yaml")


@line_bot_handler.handler.add(MessageEvent, message=TextMessageContent)
def reply_flex_msg(event):
    template = "template.json"
    template_path = os.path.join(os.path.dirname(__file__), template)
    userId = line_bot_handler.get_user_id(event)
    try:
        line_bot_handler.send_flex_message_test(userId, template_path=template_path)
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
