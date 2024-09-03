import sys
import os

# プロジェクトのルートディレクトリへのパスを追加
# これを追加しないと、src以下のモジュールをimportできない
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
)

# Flake8的には、importの順番が間違っていると警告が出るが、この順番でないと動かない
from src.api.hot_pepper import HotPepperApi

# 引数はdefaultで設定されているので、何も指定しなくてもOK
api = HotPepperApi(
    config="config.yaml",
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
    open_=True,
    close_=True,
)
condition = {
    "name": "",
    "budget": "B002, B011",
    "party_capacity": "",
    "free_drink": "1",
    "free_food": "1",
    "private_room": "0",
    "parking": "0",
    "night_view": "0",
    "lunch": "0",
    "keyword": "イタリアン",
}


print("以下の条件で検索します")
api.print_as_json(condition)
stores = api.search_restaurant_essential(condition, count=5)

print("検索結果：")
print(api.print_store_name(stores))
# print(api.print_as_json(stores))

id = ["J001232494", "J001194791", "J001052469"]
stores = api.change_if_match(id, condition, stores)

print(f"来店履歴店舗id {id}を参照して結果を変更します")
print("変更後の結果：")
print(api.print_store_name(stores))
