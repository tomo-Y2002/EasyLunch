import yaml
import builtins
import requests
import json


class HotPepperApi:
    """
    ホットペッパーグルメサーチAPIを利用するためのクラス。

    このクラスは、ホットペッパーグルメサーチAPIを使用して、
    レストラン情報を検索し、結果を処理するための機能を提供します。

    Attributes
    ----------
    API_KEY : str
        ホットペッパーグルメサーチAPIのAPIキー。
    URL : str
        APIのエンドポイントURL。
    params : dict
        APIリクエストに使用するパラメータ。

    Methods
    -------
    search_restaurant_essential(condition, count=100)
        指定された条件でレストランを検索し、結果を返します。
    print_search_result(stores)
        検索結果を整形して表示します。
    print_store_name(stores)
        店舗名のみを表示します。

    """

    # configからAPIキーを取得, お店の情報を取得する際に取得する情報を指定
    # openは、Pythonの予約語なのでopen_を利用
    def __init__(
        self,
        config="config.yaml",
        name=True,
        logo_image=True,
        name_kana=True,
        address=True,
        budget_average=True,
        budget_name=True,
        access=True,
        mobile_access=True,
        urls=True,
        photo_l=True,
        photo_s=True,
        open_=True,
        close_=True,
    ):
        """
        HotPepperApiクラスのコンストラクタ。

        Parameters
        ----------
        config : str, optional
            設定ファイルのパス。デフォルトは "config.yaml"。
        name : bool, optional
            店舗名を取得するかどうか。デフォルトは True。
        logo_image : bool, optional
            ロゴ画像を取得するかどうか。デフォルトは True。
        name_kana : bool, optional
            店舗名（カナ）を取得するかどうか。デフォルトは True。
        address : bool, optional
            住所を取得するかどうか。デフォルトは True。
        budget_average : bool, optional
            平均予算を取得するかどうか。デフォルトは True。
        budget_name : bool, optional
            予算名を取得するかどうか。デフォルトは True。
        access : bool, optional
            アクセス情報を取得するかどうか。デフォルトは True。
        mobile_access : bool, optional
            モバイル用アクセス情報を取得するかどうか。デフォルトは True。
        urls : bool, optional
            URLを取得するかどうか。デフォルトは True。
        photo_l : bool, optional
            大きい写真を取得するかどうか。デフォルトは True。
        photo_s : bool, optional
            小さい写真を取得するかどうか。デフォルトは True。
        open_ : bool, optional
            営業開始時間を取得するかどうか。デフォルトは True。
        close_ : bool, optional
            営業終了時間を取得するかどうか。デフォルトは True。

        Notes
        ----
        'open'はPythonの予約語であるため、'open_'を使用しています。

        Raises
        ----
        FileNotFoundError
            設定ファイルが見つからない場合に発生します。
        yaml.YAMLError
            YAMLファイルの解析エラーが発生した場合に発生します。
        KeyError
            設定ファイルにHOT_PEPPER_API_KEYが見つからない場合に発生します。
        """

        try:
            with builtins.open(config, "r") as file:
                self.config = yaml.safe_load(file)
            self.api_key = self.config["HOT_PEPPER_API_KEY"]
        except FileNotFoundError:
            print(f"設定ファイル '{config}' が見つかりません。")
            raise
        except yaml.YAMLError as e:
            print(f"YAMLファイルの解析エラー: {e}")
            raise
        except KeyError:
            print("設定ファイルにHOT_PEPPER_API_KEYが見つかりません。")
            raise

        self.name = name
        self.logo_image = logo_image
        self.name_kana = name_kana
        self.address = address
        self.budget_average = budget_average
        self.budget_name = budget_name
        self.access = access
        self.mobile_access = mobile_access
        self.urls = urls
        self.photo_l = photo_l
        self.photo_s = photo_s
        self.open = open_
        self.close = close_

    # condition: dict
    # ex), "condition={large_area": "Z011", "keyword": "カレー",...}
    # returns all the information of restaurants
    def search_restaurant_all(self, condition: dict, count: int = 5):
        """
        指定された条件に基づいてレストランを検索し、全ての情報を返します。

        Parameters
        ----------
        condition : dict
            検索条件を含む辞書。例: {"large_area": "Z011", "keyword": "カレー"}
        count : int, optional
            取得する結果の数。デフォルトは5。

        Returns
        -------
        list
            検索結果の店舗情報を含むリスト。各店舗の情報は辞書形式で格納されています。

        Notes
        -----
        このメソッドはHot Pepper APIを使用して検索を行います。
        APIキーは初期化時に設定ファイルから読み込まれます。
        """
        print(f"Searching restaurant by condition: {condition}")
        # リクエストURL(全員共通)
        URL = "http://webservice.recruit.co.jp/hotpepper/gourmet/v1/"
        params = {
            "key": self.api_key,
            "format": "json",
            "count": count,
            **condition,
        }
        # リクエストを送信
        response = requests.get(URL, params=params)
        # レスポンスのステータスコードを確認してエラーハンドリング
        if response.status_code == 200:
            data = response.json()
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
        # お店の情報だけをlistにして全て返す
        return data["results"]["shop"]

    # お店の情報を加工して必要な項目を取り出す
    def process_data_essential(self, stores: list):
        # process_data_essential メソッドの説明
        """
        検索結果から必要な店舗情報を抽出し、加工します。

        Parameters
        ----------
        stores (list): 検索結果の店舗情報リスト

        Returns
        ---------
        list: 必要な情報のみを含む店舗情報のリスト

        説明:
        このメソッドは、search_restaurant_all メソッドで取得した全ての店舗情報から、
        インスタンス生成時に指定された項目（name, logo_image, address など）のみを
        抽出します。各店舗の情報は辞書形式で保存され、それらをリストにまとめて返します。
        """
        # お店の情報を格納するリスト
        store_list = []
        # お店の情報を取り出す
        for store in stores:
            store_info = {}
            if self.name:
                store_info["name"] = store["name"]
            if self.logo_image:
                store_info["logo_image"] = store["logo_image"]
            if self.name_kana:
                store_info["name_kana"] = store["name_kana"]
            if self.address:
                store_info["address"] = store["address"]
            if self.budget_average:
                store_info["budget_average"] = store["budget"]["average"]
            if self.budget_name:
                store_info["budget_name"] = store["budget"]["name"]
            if self.access:
                store_info["access"] = store["access"]
            if self.mobile_access:
                store_info["mobile_access"] = store["mobile_access"]
            if self.urls:
                store_info["urls"] = store["urls"]
            if self.photo_l:
                store_info["photo_l"] = store["photo"]["mobile"]["l"]
            if self.photo_s:
                store_info["photo_s"] = store["photo"]["mobile"]["s"]
            if self.open:
                store_info["open"] = store["open"]
            if self.close:
                store_info["close"] = store["close"]
            store_list.append(store_info)
        return store_list

    # condition: dict
    # ex), "condition={large_area": "Z011", "keyword": "カレー",...}
    # returns the essential information of restaurants
    def search_restaurant_essential(self, condition: dict, count: int = 5):
        """
        指定された条件に基づいて飲食店を検索し、必要な情報のみを抽出して返します。

        Parameters
        ----------
        condition (dict): 検索条件を含む辞書。例: {"large_area": "Z011", "keyword": "カレー"}
        count (int): 取得する店舗数。デフォルトは5。

        Returns:
        ----------
        list: 各店舗の必要な情報を含む辞書のリスト。
        """
        stores = self.search_restaurant_all(condition, count)
        return self.process_data_essential(stores)

    # 結果を表示
    def print_search_result(self, stores: list):
        """
        飲食店のサーチ結果を表示します。

        Parameters
        ----------
        stores : list
            search_restaurant_essential()あるいはsearch_restaurant_all()で取得した店舗情報のリスト
        """
        print("search result:")
        print(json.dumps(stores, ensure_ascii=False, indent=2))

    # 結果の店名を表示
    def print_store_name(self, stores: list):
        """
        飲食店のサーチ結果から店名を表示します。

        Parameters
        ----------
        stores : list
            search_restaurant_essential()あるいはsearch_restaurant_all()で取得した店舗情報のリスト
        """
        print("store name:")
        for store in stores:
            print(store["name"])
