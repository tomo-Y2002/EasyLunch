import os
import sys
import yaml

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
)
from src.db.access.chat import ChatDB


def print_result(result):
    for row in result:
        print(row)


def main():
    with open("config.yaml", encoding="utf-8") as f:
        configs = yaml.safe_load(f)

    # 来店履歴DBへの接続
    chat_db = ChatDB(
        host=configs["MYSQL_HOST"],
        user=configs["MYSQL_USER"],
        password=configs["MYSQL_PASSWORD"],
        database=configs["MYSQL_DATABASE"],
    )
    conn = chat_db.connect()

    # 初期状態の確認
    result = chat_db.read(conn=conn, table="chat_history", columns=["*"])
    print_result(result)

    # データの新規作成
    print(f"----- CREATE new data in chat_history -----")
    chat_db.post(
        conn=conn,
        user_id="test456",
        speaker="BOT",
        message="飲食店をオススメできます。リクエストをどうぞ。",
    )
    chat_db.post(
        conn=conn,
        user_id="test456",
        speaker="USER",
        message="レンゲが立つくらいこってりしたラーメンが食べたいです。",
    )
    result = chat_db.read(conn=conn, table="chat_history", columns=["*"])
    print_result(result)

    # データの取得
    print(f"----- READ only user_id(= 'test456') from chat_history -----")
    result = chat_db.get(conn=conn, user_id="test456")
    print_result(result)

    # データの削除
    print(f"----- DELETE user_id(= 'test456') from chat_history -----")
    chat_db.erase(conn=conn, user_id="test456")
    result = chat_db.read(conn=conn, table="chat_history", columns=["*"])
    print_result(result)

    chat_db.commit(conn)
    chat_db.close(conn)


if __name__ == "__main__":
    main()
