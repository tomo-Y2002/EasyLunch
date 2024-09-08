from src.db.access.connector import MySQLManager


class ChatDB(MySQLManager):
    def __init__(self, host, user, password, database, is_gc=False):
        super().__init__(host, user, password, database, is_gc)
        self.table_name = "chat_history"

    def get(self, conn, user_id: str):
        """
        ユーザIDを指定して、会話履歴DBから会話履歴を取得する
        Input:
            conn: MySQLのコネクション
            user_id: ユーザID
        Output:
            会話履歴のtaple
        """
        return self.read(conn, self.table_name, ["*"], f"user_id = '{user_id}'")

    def post(self, conn, user_id: str, speaker: str, message: str):
        """
        会話履歴DBに会話履歴を追加する
        Input:
            conn: MySQLのコネクション
            user_id: ユーザID
            speaker: 発言者
            message: メッセージ
        Output:
            なし
        """
        columns = ["user_id", "speaker", "message"]
        values = [f"'{user_id}'", f"'{speaker}'", f"'{message}'"]
        self.create(conn, self.table_name, columns, values)

    def erase(self, conn, user_id: str):
        """
        ユーザIDを指定して、会話履歴DBから会話履歴を削除する
        Input:
            conn: MySQLのコネクション
            user_id: ユーザID
        Output:
            なし
        """
        self.delete(conn, self.table_name, f"user_id = '{user_id}'")
