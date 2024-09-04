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
from src.api.hot_pepper import HotPepperClient

# 引数はdefaultで設定されているので、何も指定しなくてもOK
api = HotPepperClient(
    config_path="config.yaml",
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
    "budget": "",
    "party_capacity": "",
    "free_drink": "0",
    "free_food": "0",
    "private_room": "0",
    "parking": "0",
    "night_view": "0",
    "lunch": "0",
    "keyword": "ラーメン",
}
print("以下の条件で検索します")
api.print_json(condition)

stores = api.search_essential(condition, count=15)
# storesの内容を確認
# print("以下の結果が得られました")
# api.print_as_json(stores)

print("検索結果：")
api.print_store(stores)
