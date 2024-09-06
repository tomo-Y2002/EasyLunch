import requests
import json
import yaml
import os

with open("config.yaml", encoding="utf-8") as f:
    configs = yaml.safe_load(f)

API_KEY = configs["GOOGLE_PLACES_API_KEY"]

# 場所の検索エンドポイント
search_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
search_params = {
    "input": "スターバックス",
    "inputtype": "textquery",
    "fields": "place_id",
    "key": API_KEY,
}

# 場所の検索リクエスト
response = requests.get(search_url, params=search_params)
response_data = response.json()

# レスポンスデータのデバッグ出力
print("Search Response:", json.dumps(response_data, indent=2, ensure_ascii=False))

if "candidates" in response_data and len(response_data["candidates"]) > 0:
    place_id = response_data["candidates"][0]["place_id"]
else:
    raise Exception("Place not found")

# 場所の詳細エンドポイント
details_url = "https://maps.googleapis.com/maps/api/place/details/json"
details_params = {"place_id": place_id, "fields": "name,rating,reviews", "key": API_KEY}

# 場所の詳細リクエスト
response = requests.get(details_url, params=details_params)
details = response.json()

# レスポンスデータのデバッグ出力
print("Details Response:", json.dumps(details, indent=2, ensure_ascii=False))

# 口コミデータの抽出
reviews = details.get("result", {}).get("reviews", [])
for review in reviews:
    print(
        f"Review by {review['author_name']}: {review['text']} (Rating: {review['rating']})"
    )

# レスポンスデータを JSON ファイルに保存
current_dir = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(current_dir, "place_details.json")

with open(output_file, "w", encoding="utf-8") as json_file:
    json.dump(details, json_file, ensure_ascii=False, indent=2)

print("詳細情報が place_details.json に保存されました。")
