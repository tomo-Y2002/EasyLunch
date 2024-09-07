import requests
import json
from typing import Union


class GooglePlacesClient:
    """
    Google Places APIを利用するためのクラス。
    """

    # openは、Pythonの予約語なのでopen_を利用
    def __init__(
        self,
        google_places_api_key: str,
        field_mask: dict = {
            "displayName": True,
            "id": True,
            "googleMapsUri": True,
            "rating": True,
            "location": True,
            "priceLevel": True,
            "photos": True,
        },
    ):
        """
        Google places client クラスのコンストラクタ

        Parameters
        ----------
        google_places_api_key: str,
            Google Places API Key
        field_mask: dict, optional
            Google Places APIのレスポンスから取得する情報を指定する辞書。
            デフォルトは、店舗名、ID、Google MapsのURL、評価、場所、価格レベル、写真。
        """
        self.api_key = google_places_api_key
        # field_maskのうちTrueであるキーだけをlistにする
        self.field_mask = [key for key, value in field_mask.items() if value]

    # condition: dict
    # ex), "condition={large_area": "Z011", "keyword": "カレー",...}
    # returns the essential information of restaurants
    def search_essential(self, query: str, count: int = 5):
        """
        指定された条件に基づいて飲食店を検索し、必要な情報のみを抽出して返します。

        Parameters
        ----------
        query (str),
            検索クエリ。例: "カレー"
        count (int), optional
            取得する店舗数。デフォルトは5。

        Returns:
        ----------
        list: 各店舗の必要な情報を含む辞書のリスト。
            ex) [
                    {
                        'id': 'ChIJg9-dwtaPGGARATZrumJcivI',
                        'name': '店舗名',
                        'latitude': 35.71452370573787,
                        'longitude': 139.76181006885508,
                        'rating': 4.5,
                        'urls': 'google mapのURL',
                        'priceLevel': 2,
                        'photo': '写真のURL'
                    },
                    {
                        'id': 'ChIJg9-dwtaPGGARATZrumJcivI',
                        ...
                    },
                    ...
                ]
        """

        url = "https://places.googleapis.com/v1/places:searchText"
        field_mask = ",".join(f"places.{field}" for field in self.field_mask)
        # Define the headers
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self.api_key,
            "X-Goog-FieldMask": field_mask,
        }

        data = {
            "textQuery": query,
            "languageCode": "ja",
            "locationBias": {
                "circle": {
                    "center": {
                        "latitude": 35.71452370573787,
                        "longitude": 139.76181006885508,
                    },
                    "radius": 1000.0,
                }
            },
            "pageSize": count,
            "includedType": "restaurant",
        }

        # Make the POST request
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            # Process the response
            response = response.json()["places"]
            result = []
            for store in response:
                store = self.format_result(store)
                result.append(store)
        else:
            print(f"Error: {response.status_code}, {response.text}")
        return result

    def search_with_id(self, id: str):
        """
        指定されたIDに基づいて飲食店を検索し、必要な情報のみを抽出して返します。

        Parameters
        ----------
        id (str): 店舗ID。例: "ChIJg9-dwtaPGGARATZrumJcivI"

        Returns:
        ----------
        list: 各店舗の必要な情報を含む辞書のリスト。
            ex) [
                    {
                        'id': 'ChIJg9-dwtaPGGARATZrumJcivI',
                        'name': '店舗名',
                        'latitude': 35.71452370573787,
                        'longitude': 139.76181006885508,
                        'rating': 4.5,
                        'urls': 'google mapのURL',
                        'priceLevel': 2,
                        'photo': '写真のURL'
                    }
                ]
        """
        url = "https://places.googleapis.com/v1/places/" + id
        url = "https://places.googleapis.com/v1/places/" + id
        field_mask = ",".join(self.field_mask)
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self.api_key,
            "X-Goog-FieldMask": field_mask,
        }
        params = {
            "languageCode": "ja",
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            response = response.json()
            response = self.format_result(response)
            result = []
            result.append(response)
            return result
        else:
            print(f"Error: {response.status_code}, {response.text}")

    def photo_url(self, name: str):
        """
        指定された店舗の写真のURLを取得する
        """
        max_height = 1000
        params = f"key={self.api_key}&maxHeightPx={max_height}&skipHttpRedirect=true"
        url = "https://places.googleapis.com/v1/" + name + "/media?" + params
        response = requests.get(url)
        try:
            return response.json()["photoUri"]
        except requests.exceptions.JSONDecodeError:
            print("JSONデコードエラー。レスポンスの内容:")
            print(response.text)
            return None

    def format_result(self, store: dict) -> dict:
        """
        検索結果を加工して返す
        """

        result = {}
        if "id" in store:
            result["id"] = store["id"]
        if "displayName" in store:
            result["name"] = store["displayName"]["text"]
        if "location" in store:
            result["latitude"] = store["location"]["latitude"]
        if "location" in store:
            result["longitude"] = store["location"]["longitude"]
        if "rating" in store:
            result["rating"] = store["rating"]
        if "googleMapsUri" in store:
            result["urls"] = store["googleMapsUri"]
        if "priceLevel" in store:
            result["priceLevel"] = store["priceLevel"]
        if "photos" in store:
            result["photo"] = self.photo_url(store["photos"][1]["name"])
        return result

    # 結果の店名を表示
    def print_store(self, stores: list):
        """
        飲食店のサーチ結果から店名を表示します。

        Parameters
        ----------
        stores : list
            search_essential()で取得した店舗情報のリスト
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

        # 結果を表示

    def print_json(self, data: Union[dict, str]):
        """
        list, dict, strをjsonに変換して表示
        """
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return ""
