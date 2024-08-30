import sys
import os
import json

# プロジェクトのルートディレクトリへのパスを追加
# これを追加しないと、src以下のモジュールをimportできない
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        )
    )
)
# Flake8的には、importの順番が間違っていると警告が出るが、この順番でないと動かない
from src.api.hot_pepper import HotPepperApi

api = HotPepperApi()
condition = {"large_area": "Z011", "keyword": "カレー"}
stores = api.search_restaurant_essencial(condition)

# storesの内容を確認
print("stores の内容:")
print(json.dumps(stores, ensure_ascii=False, indent=2))
# storesの中から店名を抜き出して表示
for store in stores:
    print(store["name"])
