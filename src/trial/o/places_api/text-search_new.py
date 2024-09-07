import requests
import json
import yaml
import os

with open("config.yaml", encoding="utf-8") as f:
    configs = yaml.safe_load(f)

API_KEY = configs["GOOGLE_PLACES_API_KEY"]


def find_place(query, api_key):
    # Define the API endpoint
    url = "https://places.googleapis.com/v1/places:searchText"

    # Define the headers
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "places.displayName",
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
        "pageSize": 5,
        "includedType": "restaurant",
    }

    # Make the POST request
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        # Process the response
        print(response.json())
        current_dir = os.path.dirname(os.path.abspath(__file__))
        output_file = os.path.join(current_dir, "place_details.json")
        with open(output_file, "w", encoding="utf-8") as json_file:
            json.dump(response.json(), json_file, ensure_ascii=False, indent=2)
        print("詳細情報が place_details.json に保存されました。")
    else:
        print(f"Error: {response.status_code}, {response.text}")

    return json.loads(response.text)


if __name__ == "__main__":
    find_place("濃厚豚骨ラーメン", API_KEY)
