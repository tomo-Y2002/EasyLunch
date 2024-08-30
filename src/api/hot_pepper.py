class HotPepperApi:
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
        import yaml
        import builtins

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
        import requests

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
    def process_data_essencial(self, stores: list):
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
    def search_restaurant_essencial(self, condition: dict, count: int = 5):
        stores = self.search_restaurant_all(condition, count)
        return self.process_data_essencial(stores)

    # Line messaging APIに送信するために、出力をさらに加工する関数を用意する?

    # お店の情報をdbに保存する関数を用意する？

    # ランキングをdbから取得した情報に応じて変更する関数を用意する？
