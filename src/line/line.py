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
    """
    LINEメッセージングAPIを操作するためのクラス。

    このクラスは、LINEメッセージングAPIを使用して、メッセージの送信、受信、
    およびWebhookの処理を行うための機能を提供します。

    Attributes
    ----------
    line_channel_secret : str
        LINEチャンネルのシークレットキー
    line_channel_access_token : str
        LINEチャンネルのアクセストークン
    port : int
        サーバーのポート番号
    handler : WebhookHandler
        LINEのWebhookを処理するハンドラー
    configuration : Configuration
        LINEメッセージングAPIの設定

    Methods
    -------
    __init__(config="config.yaml")
        クラスのインスタンスを初期化し、設定を読み込みます。
    handle_webhook(body, signature)
        Webhookのリクエストを処理します。
    get_user_id(event)
        イベントからユーザーIDを取得します。
    send_text_message(user_id, text)
        指定されたユーザーにテキストメッセージを送信します。
    reply_to_message_rsp(event)
        じゃんけんの返信を行います。
    send_flex_message_test(user_id, template)
        Flexメッセージのテストを行います。

    Notes
    -----
    このクラスを使用する前に、適切な設定ファイルが必要です。
    設定ファイルには、LINEチャンネルのシークレットキー、アクセストークン、
    およびサーバーのポート番号が含まれている必要があります。
    """

    def __init__(self, config="config.yaml"):
        """
        LineMessagingApiクラスのコンストラクタ。

        設定ファイルを読み込み、LINEメッセージングAPIの初期設定を行います。

        Parameters
        ----------
        config : str, optional
            設定ファイルのパス。デフォルトは "config.yaml"。

        Raises
        ------
        FileNotFoundError
            設定ファイルが見つからない場合。
        yaml.YAMLError
            YAMLファイルの解析エラーが発生した場合。
        KeyError
            必要な設定キー（LINE_CHANNEL_SECRET, LINE_CHANNEL_ACCESS_TOKEN, PORT）が
            見つからない場合。
        Exception
            WebhookHandlerまたはConfigurationの初期化エラーが発生した場合。

        Notes
        -----
        このメソッドは以下の属性を初期化します：
        - line_channel_secret
        - line_channel_access_token
        - port
        - handler (WebhookHandler)
        - configuration (Configuration)
        """
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
        """
        Webhookのリクエストを処理します。

        Parameters
        ----------
        body : str
            Webhookリクエストのボディ。
        signature : str
            リクエストの署名。

        Raises
        ------
        Exception
            Webhookの処理中にエラーが発生した場合。

        Notes
        -----
        このメソッドは、LINEプラットフォームからのWebhookリクエストを
        処理します。署名を検証し、ボディの内容を適切に処理します。
        """
        try:
            self.handler.handle(body, signature)
        except Exception as e:
            print(f"ウェブフック処理エラー(handle_webhook): {e}")

    def reply_to_message_rsp(self, event):
        """
        じゃんけんの手に対して勝つ手を返信します。

        Parameters
        ----------
        event : MessageEvent
            LINEプラットフォームから受け取ったメッセージイベント。

        Returns
        -------
        None

        Raises
        ------
        Exception
            メッセージの送信中にエラーが発生した場合。

        Notes
        -----
        このメソッドは、ユーザーが送信したじゃんけんの手（グー、チョキ、パー）に対して、
        必ず勝つ手を返信します。それ以外のメッセージには対応していません。
        """
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
        """
        送信されたメッセージからユーザーIDを取得します。

        Parameters
        ----------
        event : MessageEvent
            LINEプラットフォームから受け取ったメッセージイベント。

        Returns
        -------
        str
            メッセージを送信したユーザーのID。

        Notes
        -----
        このメソッドは、イベントオブジェクトからユーザーIDを抽出します。
        グループやルームからのメッセージの場合も、個別のユーザーIDを返します。
        """
        return event.source.user_id

    # 指定したmsgを指定したuserIdの人に送信する
    def send_text_message(self, userId, msg):
        """
        指定したメッセージを指定したユーザーIDの人に送信します。

        Parameters
        ----------
        userId : str
            メッセージを送信する対象のユーザーID。
        msg : str
            送信するメッセージの内容。

        Returns
        -------
        なし

        Notes
        -----
        このメソッドは、指定されたユーザーIDに対してプッシュメッセージを送信します。
        エラーが発生した場合は、エラーメッセージをコンソールに出力します。
        """
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
        """
        指定したユーザーIDにFlexメッセージを送信するためのテスト関数です。

        Parameters
        ----------
        userId : str
            メッセージを送信する対象のユーザーID。
        template : str, optional
            Flexメッセージのテンプレートファイルのパス。デフォルトは"template.json"。

        Returns
        -------
        なし

        Notes
        -----
        この関数は、指定されたテンプレートファイルからFlexメッセージの内容を読み込み、
        指定されたユーザーIDに対してプッシュメッセージとして送信します。
        テンプレートファイルが見つからない場合や、JSONの解析エラー、
        メッセージ送信時のエラーが発生した場合は、適切な例外を発生させます。
        """
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
