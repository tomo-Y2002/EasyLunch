from src.db.access.connector import MySQLManager


class VisitDB(MySQLManager):
    def __init__(self, host, user, password, database):
        super().__init__(host, user, password, database)
        self.table_name = "visit_history"

    def get(self, conn, user_id: str):
        """
        ユーザIDを指定して、来店履歴DBから来店履歴を取得する
        Input:
            conn: MySQLのコネクション
            user_id: ユーザID
        Output:
            来店履歴のtaple
        """
        return self.read(conn, self.table_name, ["*"], f"user_id = '{user_id}'")

    def post(self, conn, user_id: str, store_id: str):
        """
        来店履歴DBに来店履歴を追加する
        Input:
            conn: MySQLのコネクション
            user_id: ユーザID
            store_id: 店舗ID
        Output:
            なし
        """
        columns = ["user_id", "store_id"]
        values = [f"'{user_id}'", f"'{store_id}'"]
        self.create(conn, self.table_name, columns, values)
