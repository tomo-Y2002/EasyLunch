import os
import sys
import yaml

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
)
from src.db.access.visit import VisitDB


def print_result(result):
    for row in result:
        print(row)


def main():
    with open("config.yaml", encoding="utf-8") as f:
        configs = yaml.safe_load(f)

    # 来店履歴DBへの接続
    visit_db = VisitDB(
        host=configs["MYSQL_HOST"],
        user=configs["MYSQL_USER"],
        password=configs["MYSQL_PASSWORD"],
        database=configs["MYSQL_DATABASE"],
    )
    conn = visit_db.connect()

    # 初期状態の確認
    result = visit_db.read(conn=conn, table="visit_history", columns=["*"])
    print_result(result)

    # データの新規作成
    print(f"----- CREATE new data in visit_history -----")
    visit_db.post(conn=conn, user_id="test123", store_id="JKrolling123")
    result = visit_db.read(conn=conn, table="visit_history", columns=["*"])
    print_result(result)

    # データの取得
    print(f"----- READ only user_id(= 'test123') from visit_history -----")
    result = visit_db.get(conn=conn, user_id="test123")
    print_result(result)

    visit_db.commit(conn)
    visit_db.close(conn)


if __name__ == "__main__":
    main()
