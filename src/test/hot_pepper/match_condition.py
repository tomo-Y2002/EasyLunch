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
    "private_room": "1",
    "parking": "1",
    "night_view": "1",
    "lunch": "1",
    "keyword": "イタリアン",
}
stores = api.search_restaurant_essential(condition, count=15)

print("以下の条件で検索しました")
api.print_as_json(condition)
id1 = stores[0]["id"]
match1 = api.match_condition(id1, condition)
print(f"店舗id {id1}は、", end="")
if match1:
    print("条件に一致しました")
else:
    print("条件に一致しません")

id2 = "aaaaaaaaaa"
match2 = api.match_condition(id2, condition)
print(f"店舗id {id2}は", end="")
if match2:
    print("条件に一致しました")
else:
    print("条件に一致しません")
