import sys
import os
import yaml

# プロジェクトのルートディレクトリへのパスを追加
# これを追加しないと、src以下のモジュールをimportできない
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
)

# Flake8的には、importの順番が間違っていると警告が出るが、この順番でないと動かない
from src.api.hot_pepper import HotPepperClient

# 引数はdefaultで設定されているので、何も指定しなくてもOK
with open("config.yaml", encoding="utf-8") as f:
    configs = yaml.safe_load(f)
api = HotPepperClient(
    hot_pepper_api_key=configs["HOT_PEPPER_API_KEY"],
    hot_pepper_lat=configs["HOT_PEPPER_LAT"],
    hot_pepper_lng=configs["HOT_PEPPER_LNG"],
    hot_pepper_range=configs["HOT_PEPPER_RANGE"],
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
    photo_pc_s=True,
    photo_pc_m=True,
    open_=True,
    close_=True,
)
condition = {
    "name": "",
    "budget": "",
    "party_capacity": "",
    "free_drink": "",
    "free_food": "",
    "private_room": "0",
    "parking": "0",
    "night_view": "0",
    "keyword": "イタリアン",
}
print("以下の条件で検索します")
api.print_json(condition)

stores = api.search_essential(condition, count=15)
# storesの内容を確認
# print("以下の結果が得られました")
# api.print_json(stores)

print("検索結果：")
api.print_store(stores)
