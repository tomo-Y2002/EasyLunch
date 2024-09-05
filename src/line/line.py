import yaml
import json
from linebot.v3.webhook import WebhookHandler
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    TextMessage,
    PushMessageRequest,
)
import requests
import copy


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
    get_user_id(event)
        イベントからユーザーIDを取得します。
    send_text_message(user_id, text)
        指定されたユーザーにテキストメッセージを送信します。
    send_flex_message_test(user_id, template)
        Flexメッセージのテストを行います。

    Notes
    -----
    このクラスを使用する前に、適切な設定ファイルが必要です。
    設定ファイルには、LINEチャンネルのシークレットキー、アクセストークン、
    およびサーバーのポート番号が含まれている必要があります。
    """

    def __init__(self, config_path="config.yaml"):
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
            with open(config_path, "r", encoding="utf-8") as file:
                config = yaml.safe_load(file)
        except FileNotFoundError:
            print(f"設定ファイル '{config_path}' が見つかりません。")
            raise
        except yaml.YAMLError as e:
            print(f"YAMLファイルの解析エラー: {e}")
            raise

        if "LINE_CHANNEL_SECRET" not in config:
            raise KeyError("LINE_CHANNEL_SECRETがconfig fileに定義されていません。")
        if "LINE_CHANNEL_ACCESS_TOKEN" not in config:
            raise KeyError(
                "LINE_CHANNEL_ACCESS_TOKENがconfig fileに定義されていません。"
            )
        if "PORT" not in config:
            raise KeyError("PORTがconfig fileに定義されていません。")
        self.line_channel_secret = config["LINE_CHANNEL_SECRET"]
        self.line_channel_access_token = config["LINE_CHANNEL_ACCESS_TOKEN"]
        self.port = int(config["PORT"])

        try:
            self.handler = WebhookHandler(config["LINE_CHANNEL_SECRET"])
        except Exception as e:
            print(f"WebhookHandlerの初期化エラー(LineMessagingApi.init): {e}")
            raise

        try:
            self.configuration = Configuration(
                access_token=config["LINE_CHANNEL_ACCESS_TOKEN"]
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

    # 送信されたメッセージからuserIdを取得する
    def get_id(self, event):
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
    def send_text(self, userId, content):
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
                    PushMessageRequest(to=userId, messages=[msg])
                )
                # print(f"{userId}にメッセージ送信(send_text_message): {msg}")
            except Exception as e:
                print(f"メッセージ送信エラー: {e}")

    # send_FM.pyが動いたら消去予定
    def send_flex_test(self, userId, template_path="template.json"):
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
            with open(template_path, "r", encoding="utf-8") as f:
                contents = json.load(f)
        except json.JSONDecodeError as e:
            print(f"JSONファイルの解析エラー: {e}")
            raise
        except FileNotFoundError:
            print(f"テンプレートファイル '{template_path}' が見つかりません。")
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
            print(f"Flex Message送信エラー: {e}")

    def create_carousel(
        self, userId: str, stores: list, template_path="./src/line/template.json"
    ) -> str:
        """
        storesのリストをもとに、flex messageを作成する関数

        Parameters
        ----------
        stores : list
            ストアのリスト
        template_path : str, optional
            Flexメッセージのテンプレートファイルのパス。デフォルトは"./src/line/template.json"。

        Returns
        -------
        data : str
            flex message
        """
        data = {"type": "carousel", "contents": []}
        try:
            with open(template_path, "r", encoding="utf-8") as f:
                template = json.load(f)
        except FileNotFoundError:
            print(f"テンプレートファイル '{template_path}' が見つかりません。")
            raise
        except json.JSONDecodeError as e:
            print(f"JSONファイルの解析エラー: {e}")
            raise
        except Exception as e:
            print(f"予期せぬエラーが発生しました: {e}")
            raise

        for store in stores:
            contents_format = copy.deepcopy(template)
            name = store["name"]
            img = store["photo_l"]
            catch = store["catch"]
            address = store["address"]
            price = store["budget_name"]
            uri = store["urls"]
            id = store["id"]
            contents_format["header"]["contents"][0]["text"] = name
            contents_format["hero"]["url"] = img
            contents_format["body"]["contents"][1]["contents"][0]["text"] = catch
            contents_format["body"]["contents"][3]["text"] = address
            contents_format["body"]["contents"][4]["text"] = price
            contents_format["body"]["contents"][5]["contents"][0]["action"]["uri"] = uri
            contents_format["body"]["contents"][5]["contents"][1]["action"]["data"] = (
                "店のid" + id
            )

            data["contents"].append(contents_format)

        carousel = {
            # userIDを指定。
            "to": userId,
            "messages": [
                {
                    "type": "flex",
                    "altText": "This is a Flex Message",
                    "contents": data,
                }
            ],
        }
        return carousel

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
