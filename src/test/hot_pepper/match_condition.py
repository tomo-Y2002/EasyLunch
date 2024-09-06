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
    photo_pc_l=True,
    photo_pc_s=True,
    open_=True,
    close_=True,
)
condition = {
    "name": "",
    "budget": "B002, B011",
    "party_capacity": "",
    "free_drink": "0",
    "free_food": "0",
    "private_room": "0",
    "parking": "0",
    "night_view": "0",
    "lunch": "0",
    "keyword": "",
}
stores = api.search_essential(condition, count=15)
print("以下の条件で検索しました")
api.print_json(condition)

print("検索結果：")
api.print_store(stores)
# 最初の店が存在するなら、その店舗のidを取得して、条件に一致するかどうかを確認する
if stores:
    id1 = stores[0]["id"]
    match1 = api.match_condition(id1, condition)
    print(f"店舗id {id1}は、", end="")
    if match1:
        print("条件に一致しました")
    else:
        print("条件に一致しません")
else:
    print("店舗情報がありません")

id2 = "aaaaaaaaaa"
match2 = api.match_condition(id2, condition)
print(f"店舗id {id2}は、", end="")
if match2:
    print("条件に一致しました")
else:
    print("条件に一致しません")
