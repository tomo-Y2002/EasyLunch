from flask import Flask, abort, request
from linebot.v3.webhook import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent
import yaml

with open("../../../config.yaml", "r") as f:
    config = yaml.safe_load(f)
LINE_CHANNEL_SECRET = config["LINE_CHANNEL_SECRET"]
LINE_CHANNEL_ACCESS_TOKEN = config["LINE_CHANNEL_ACCESS_TOKEN"]
PORT = config["PORT"]

app = Flask(__name__)
handler = WebhookHandler(LINE_CHANNEL_SECRET)
configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)


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
        app.logger.info(
            "Invalid signature. Please check your channel access token/channel secret."
        )
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        # 相手の送信した内容で条件分岐して回答を変数に代入
        if event.message.text == "グー":
            msg = "パー"
        elif event.message.text == "チョキ":
            msg = "グー"
        elif event.message.text == "パー":
            msg = "チョキ"
        else:
            msg = "ごめんね。\nまだ他のメッセージには対応してないよ"

        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token, messages=[TextMessage(text=msg)]
            )
        )


if __name__ == "__main__":
    port = PORT if PORT else 5000
    app.logger.info(f"Starting server on port {port}")
    app.run(host="0.0.0.0", port=port, debug=True)
