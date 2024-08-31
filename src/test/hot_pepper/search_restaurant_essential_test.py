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
    name=True,
    logo_image=True,
    name_kana=True,
    address=True,
    budget_average=True,
    budget_name=True,
    access=True,
    mobile_access=True,
    urls=True,
    photo_l=True,
    photo_s=True,
    open_=True,
    close_=True,
)
condition = {"large_area": "Z011", "keyword": "カレー"}
stores = api.search_restaurant_essential(condition, count=5)

# storesの内容を確認
api.print_search_result(stores)
api.print_store_name(stores)
