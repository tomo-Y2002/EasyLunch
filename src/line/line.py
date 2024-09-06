from linebot.v3.webhook import WebhookHandler
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    TextMessage,
    PushMessageRequest,
)
import requests


class LineMessagingClient:
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
    send_text(user_id, text)
        指定されたユーザーにテキストメッセージを送信します。
    send_flex(data)
        Flexメッセージのテストを行います。

    Notes
    -----
    このクラスを使用する前に、適切な設定ファイルが必要です。
    設定ファイルには、LINEチャンネルのシークレットキー、アクセストークン、
    およびサーバーのポート番号が含まれている必要があります。
    """

    def __init__(
        self,
        line_channel_secret: str,
        line_channel_access_token: str,
        port: int,
    ):
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
        self.line_channel_secret = line_channel_secret
        self.line_channel_access_token = line_channel_access_token
        self.port = port

        try:
            self.handler = WebhookHandler(channel_secret=self.line_channel_secret)
        except Exception as e:
            print(f"WebhookHandlerの初期化エラー(LineMessagingApi.init): {e}")
            raise

        try:
            self.configuration = Configuration(
                access_token=self.line_channel_access_token
            )
        except Exception as e:
            print(f"Configurationの初期化エラー: {e}")
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

    # 指定したmsgを指定したuserIdの人に送信する
    def send_text(self, user_id, content):
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
                msg = TextMessage(text=content)
                line_bot_api = MessagingApi(api_client)
                line_bot_api.push_message_with_http_info(
                    PushMessageRequest(to=user_id, messages=[msg])
                )
                # print(f"{userId}にメッセージ送信(send_text_message): {msg}")
            except Exception as e:
                print(f"メッセージ送信エラー: {e}")

    def send_flex(self, data: str):
        """
        作成されたflex messageを送信する関数

        Parameters
        -----------
        data : str
            フレックスメッセージ
        """

        access_token = self.line_channel_access_token
        url = "https://api.line.me/v2/bot/message/push"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + access_token,
        }
        response = requests.post(url, headers=headers, json=data)
        print(response.status_code)
