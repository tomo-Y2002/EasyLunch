import os
import sys
import yaml

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
)

from src.api.google_places import GooglePlacesClient

with open("config.yaml", encoding="utf-8") as f:
    configs = yaml.safe_load(f)

client = GooglePlacesClient(google_places_api_key=configs["GOOGLE_PLACES_API_KEY"])
query = "濃厚豚骨ラーメン"
results = client.search_essential(query)
if len(results) > 0:
    print(f"{query}を条件としてヒットした一つ目の店舗の情報：")
    print(f"    name:{results[0]['name']}")
    print(f"    rating:{results[0]['rating']}")
    print(f"    priceLevel:{results[0]['priceLevel']}")
    print(f"    photo:{results[0]['photo']}")

    print("----------------------------------------")
    print(f"id={results[0]['id']}の店舗の情報")
    results = client.search_with_id(results[0]["id"])
    print(f"    name:{results[0]['name']}")
    print(f"    rating:{results[0]['rating']}")
    print(f"    priceLevel:{results[0]['priceLevel']}")
    print(f"    photo:{results[0]['photo']}")
else:
    print("検索結果がありません。")
