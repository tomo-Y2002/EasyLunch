import requests
import yaml

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# print(config["HOT_PEPPER_API_KEY"])

# リクエストURL(全員共通)
URL = "http://webservice.recruit.co.jp/hotpepper/gourmet/v1/"

API_KEY = config["HOT_PEPPER_API_KEY"]

# keywordは、最低1つ以上必要なパラメータの中からキーワード検索を選択
# json形式でデータが欲しいので、任意のパラメータformatを指定
# データが15件欲しいので、countを指定
body = {"key": API_KEY, "keyword": "カレー", "format": "json", "count": 15}

response = requests.get(URL, body)
# 取得したデータからJSONを取得
datum = response.json()
# JSONデータからお店のデータを取得
stores = datum["results"]["shop"]
# お店の中から店名を抜き出して表示
for store_name in stores:
    name = store_name["name"]
    print(name)
