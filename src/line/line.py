import yaml
import json
from linebot.v3.webhook import WebhookHandler
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    PushMessageRequest,
)
import requests


class LineMessagingApi:
    def __init__(self, config="config.yaml"):
        try:
            with open(config, "r") as file:
                config_ = yaml.safe_load(file)
        except FileNotFoundError:
            print(f"設定ファイル '{config}' が見つかりません。(LineMessagingApi.init)")
            raise
        except yaml.YAMLError as e:
            print(f"YAMLファイルの解析エラー(LineMessagingApi.init): {e}")
            raise

        if "LINE_CHANNEL_SECRET" not in config_:
            raise KeyError(
                "LINE_CHANNEL_SECRETがconfig fileに定義されていません。(LineMessagingApi.init)"
            )
        if "LINE_CHANNEL_ACCESS_TOKEN" not in config_:
            raise KeyError(
                "LINE_CHANNEL_ACCESS_TOKENがconfig fileに定義されていません。(LineMessagingApi.init)"
            )
        if "PORT" not in config_:
            raise KeyError(
                "PORTがconfig fileに定義されていません。(LineMessagingApi.init)"
            )
        self.line_channel_secret = config_["LINE_CHANNEL_SECRET"]
        self.line_channel_access_token = config_["LINE_CHANNEL_ACCESS_TOKEN"]
        self.port = int(config_["PORT"])

        try:
            self.handler = WebhookHandler(config_["LINE_CHANNEL_SECRET"])
        except Exception as e:
            print(f"WebhookHandlerの初期化エラー(LineMessagingApi.init): {e}")
            raise

        try:
            self.configuration = Configuration(
                access_token=config_["LINE_CHANNEL_ACCESS_TOKEN"]
            )
        except Exception as e:
            print(f"Configurationの初期化エラー(LineMessagingApi.init): {e}")
            raise

    def handle_webhook(self, body, signature):
        try:
            self.handler.handle(body, signature)
        except Exception as e:
            print(f"ウェブフック処理エラー(handle_webhook): {e}")

    def reply_to_message_rsp(self, event):
        with ApiClient(self.configuration) as api_client:
            if event.message.text == "グー":
                msg = "パー"
            elif event.message.text == "チョキ":
                msg = "グー"
            elif event.message.text == "パー":
                msg = "チョキ"
            else:
                msg = "ごめんね。\nまだ他のメッセージには対応してないよ"

            try:
                line_bot_api = MessagingApi(api_client)
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(
                        reply_token=event.reply_token, messages=[TextMessage(text=msg)]
                    )
                )
                # print(f"メッセージ送信(reply_to_message_rsp): {msg}")
            except Exception as e:
                print(f"メッセージ送信エラー(reply_to_message_rsp): {e}")

    # 送信されたメッセージからuserIdを取得する
    def get_user_id(self, event):
        return event.source.user_id

    # 指定したmsgを指定したuserIdの人に送信する
    def send_text_message(self, userId, msg):
        with ApiClient(self.configuration) as api_client:
            try:
                msg = TextMessage(text="受け取りました")
                line_bot_api = MessagingApi(api_client)
                line_bot_api.push_message_with_http_info(
                    PushMessageRequest(to=userId, messages=[msg])
                )
                # print(f"{userId}にメッセージ送信(send_text_message): {msg}")
            except Exception as e:
                print(f"メッセージ送信エラー(send_text_message): {e}")

    def send_flex_message_test(self, userId, template="template.json"):
        try:
            with open(template, "r") as f:
                contents = json.load(f)
        except json.JSONDecodeError as e:
            print(f"JSONファイルの解析エラー(send_flex_message_test): {e}")
            raise
        except FileNotFoundError:
            print(
                f"テンプレートファイル '{template}' が見つかりません。(send_flex_message_test)"
            )
            raise

        access_token = self.line_channel_access_token
        url = "https://api.line.me/v2/bot/message/push"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + access_token,
        }
        data = {
            # userIDを指定。
            "to": userId,
            "messages": [
                {
                    "type": "flex",
                    "altText": "This is a Flex Message",
                    # contentsの内容はjsonファイルから読み込める
                    "contents": contents,
                }
            ],
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()  # HTTPエラーがあれば例外を発生させる
        except requests.RequestException as e:
            print(f"Flex Message送信エラー(send_flex_message_test): {e}")

    # ToDo: 以下の関数を実装する
    #   json形式のtextを入力として、flex_messageのjson形式に埋め込むための関数 : create_flex_message(self, text) -> contents
    #   flex_messageを送信するための関数: send_flex_message(self, userId, contents)
