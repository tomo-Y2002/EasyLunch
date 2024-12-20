import yaml

from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
)
import os

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

app = Flask(__name__)

# 環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = config["LINE_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = config["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN, "http://localhost:8080")
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@app.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=event.message.text)
    )


if __name__ == "__main__":
    # app.run()
    port = int(os.getenv("PORT", config["PORT"]))
    app.run(host="0.0.0.0", port=port)
