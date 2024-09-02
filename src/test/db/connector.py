import os
import sys
import yaml

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
)
from src.db.access.connector import MySQLManager


def print_result(result):
    for row in result:
        print(row)


def main():
    with open("config.yaml", encoding="utf-8") as f:
        configs = yaml.safe_load(f)

    manager = MySQLManager(
        host=configs["MYSQL_HOST"],
        user=configs["MYSQL_USER"],
        password=configs["MYSQL_PASSWORD"],
        database=configs["MYSQL_DATABASE"],
    )
    conn = manager.connect()

    result = manager.execute(conn=conn, query="SELECT * FROM chat_history")
    print_result(result)

    # データの新規作成
    print(f"----- CREATE new data in chat_history -----")
    result = manager.create(
        conn=conn,
        table="chat_history",
        columns=["user_id", "message", "speaker"],
        values=["'test123'", "'Hello, World!'", "'BOT'"],
    )
    result = manager.read(conn=conn, table="chat_history", columns=["*"])
    print_result(result)

    # データの取得
    print(f"----- READ only history_id from chat_history -----")
    result = manager.read(conn=conn, table="chat_history", columns=["history_id"])
    print_result(result)

    # データの更新
    print(f"----- UPDATE chat_history -----")
    result = manager.update(
        conn,
        table="chat_history",
        columns=["message", "speaker"],
        values=["'めっちゃうまいラーメン屋でした'", "'USER'"],
        condition="user_id = 'test123'",
    )
    result = manager.read(conn=conn, table="chat_history", columns=["*"])
    print_result(result)

    # データの削除
    print(f"----- DELETE chat_history -----")
    result = manager.delete(conn, table="chat_history", condition="user_id = 'test123'")
    result = manager.read(conn=conn, table="chat_history", columns=["*"])
    print_result(result)

    # コミットとクローズ
    manager.commit(conn)
    manager.close(conn)


if __name__ == "__main__":
    main()
