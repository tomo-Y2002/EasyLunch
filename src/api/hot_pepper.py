import requests
import json
from typing import Union


class HotPepperClient:
    """
    ホットペッパーグルメサーチAPIを利用するためのクラス。

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
        hot_pepper_api_key: str,
        hot_pepper_lat: str,
        hot_pepper_lng: str,
        hot_pepper_range: str,
        id=True,
        name=True,
        logo_image=True,
        name_kana=True,
        address=True,
        budget_average=True,
        budget_name=True,
        catch=True,
        access=True,
        mobile_access=True,
        urls=True,
        photo_l=True,
        photo_s=True,
        photo_pc_l=True,
        photo_pc_m=True,
        photo_pc_s=True,
        open_=True,
        close_=True,
    ):
        """
        HotPepperClientクラスのコンストラクタ。

        Parameters
        ----------
        config_path : str, optional
            設定ファイルのパス。デフォルトは "config.yaml"。
        id : bool, optional
            お店IDを取得するかどうか。デフォルトは True。
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
        catch : bool, optional
            キャッチコピーを取得するかどうか。デフォルトは True。
        access : bool, optional
            アクセス情報を取得するかどうか。デフォルトは True。
        mobile_access : bool, optional
            モバイル用アクセス情報を取得するかどうか。デフォルトは True。
        urls : bool, optional
            URLを取得するかどうか。デフォルトは True。
        photo_l : bool, optional
            大きい写真を取得するかどうか。デフォルトは True。
        photo_pc_m : bool, optional
            pc用の中くらいの写真を取得するかどうか。デフォルトは True。
        photo_s : bool, optional
            小さい写真を取得するかどうか。デフォルトは True。
        photo_pc_l : bool, optional
            pc用の大きい写真を取得するかどうか。デフォルトは True。
        photo_pc_s : bool, optional
            pc用の小さい写真を取得するかどうか。デフォルトは True。
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

        self.api_key = hot_pepper_api_key
        self.lat = hot_pepper_lat
        self.lng = hot_pepper_lng
        self.range = hot_pepper_range
        self.id = id
        self.name = name
        self.logo_image = logo_image
        self.name_kana = name_kana
        self.address = address
        self.budget_average = budget_average
        self.budget_name = budget_name
        self.catch = catch
        self.access = access
        self.mobile_access = mobile_access
        self.urls = urls
        self.photo_l = photo_l
        self.photo_s = photo_s
        self.photo_pc_l = photo_pc_l
        self.photo_pc_m = photo_pc_m
        self.photo_pc_s = photo_pc_s
        self.open = open_
        self.close = close_

    # condition: dict
    # ex), "condition={large_area": "Z011", "keyword": "カレー",...}
    # returns all the information of restaurants
    def search_all(self, condition: dict, count: int = 5):
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
        # リクエストURL(全員共通)
        URL = "http://webservice.recruit.co.jp/hotpepper/gourmet/v1/"

        # 小エリアを条件に追加
        condition["lat"] = self.lat
        condition["lng"] = self.lng
        condition["range"] = self.range
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
    def filter_stores(self, stores: list):
        """
        検索結果から必要な店舗情報を抽出し、加工します。

        Parameters
        ----------
        stores (list): 検索結果の店舗情報リスト

        Returns
        ---------
        list: 必要な情報のみを含む店舗情報のリスト

        説明:
        このメソッドは、search_all メソッドで取得した全ての店舗情報から、
        インスタンス生成時に指定された項目（name, logo_image, address など）のみを
        抽出します。各店舗の情報は辞書形式で保存され、それらをリストにまとめて返します。
        """
        # お店の情報を格納するリスト
        store_list = []
        # お店の情報を取り出す
        for store in stores:
            store_info = {}
            if self.id:
                store_info["id"] = store["id"]
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
            if self.catch:
                store_info["catch"] = store["catch"]
            if self.access:
                store_info["access"] = store["access"]
            if self.mobile_access:
                store_info["mobile_access"] = store["mobile_access"]
            if self.urls:
                store_info["urls"] = store["urls"]["pc"]
            if self.photo_l:
                store_info["photo_l"] = store["photo"]["mobile"]["l"]
            if self.photo_s:
                store_info["photo_s"] = store["photo"]["mobile"]["s"]
            if self.photo_pc_l:
                store_info["photo_pc_l"] = store["photo"]["pc"]["l"]
            if self.photo_pc_m:
                store_info["photo_pc_m"] = store["photo"]["pc"]["m"]
            if self.photo_pc_s:
                store_info["photo_pc_s"] = store["photo"]["pc"]["s"]
            if self.open:
                store_info["open"] = store["open"]
            if self.close:
                store_info["close"] = store["close"]
            store_list.append(store_info)
        return store_list

    # condition: dict
    # ex), "condition={large_area": "Z011", "keyword": "カレー",...}
    # returns the essential information of restaurants
    def search_essential(self, condition: dict, count: int = 5):
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
        stores = self.search_all(condition, count)
        return self.filter_stores(stores)

    # 結果を表示
    def print_json(self, data: Union[list, dict, str]):
        """
        list, dict, strをjsonに変換して表示
        """
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return ""

    # 結果の店名を表示
    def print_store(self, stores: list):
        """
        飲食店のサーチ結果から店名を表示します。

        Parameters
        ----------
        stores : list
            search_essential()あるいはsearch_all()で取得した店舗情報のリスト
        """
        # print("store name:")
        if not stores:
            print("店舗情報がありません。")
            return ""

        for store in stores:
            if isinstance(store, dict) and "name" in store:
                print(store["name"])
            else:
                print("不正なストア形式:", store)

        # Noneを返さないようにする
        return ""

    def match_condition(self, shop_id: str, condition: dict) -> bool:
        """
        指定された店舗IDが条件に一致するかどうかを確認します。

        Parameters
        ----------
        shop_id : str
            店舗ID
        condition : dict
            検索条件を含む辞書。例: {"large_area": "Z011", "keyword": "カレー"}

        Returns
        -------
        bool: 店舗idで指定した店が条件に一致する場合はTrue, そうでない場合はFalse
        """
        # conditionにidの条件を追加
        condition["id"] = shop_id
        # 条件に基づいて店舗情報を検索
        stores = self.search_essential(condition)
        if stores:
            return True
        else:
            return False

    def rerank(self, shop_ids: list, condition: dict, stores: list) -> list:
        """
        来店履歴の店舗idが条件に一致する場合は、storesの最後をその店舗の情報に変更します。

        Parameters
        ----------
        shop_ids : list
            店舗IDのリスト
        condition : dict
            検索条件を含む辞書。例: {"large_area": "Z011", "keyword": "カレー"}
        stores : list
            店舗情報のリスト

        Returns
        -------
        list: 変更後のstores
        """
        # storesからshop_idのリストを取り出す
        shop_ids_in_stores = [store["id"] for store in stores]
        for shop_id in shop_ids:
            if self.match_condition(shop_id, condition):
                # その店舗がstoresにまだ入っていない場合は最後を入れ替え
                if shop_id not in shop_ids_in_stores:
                    stores[-1] = self.search_essential({"id": shop_id}, count=1)[0]
        return stores
