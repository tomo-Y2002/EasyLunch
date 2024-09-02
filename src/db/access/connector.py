import mysql.connector


class MySQLConnector:
    """
    MySQL のサーバに接続するクラス
    """

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        """
        データベースへの接続を行う
        """
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
        )

    def close(self, conn):
        """
        データベースへの接続を閉じる
        """
        conn.close()

    def commit(self, conn):
        """
        トランザクションをコミットする
        """
        conn.commit()

    def execute(self, conn, query):
        """
        クエリを実行する
        """
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result


class MySQLManager(MySQLConnector):
    """
    MySQLのDBに対して CRUD 操作を行うクラス
    """

    def __init__(self, host, user, password, database):
        super().__init__(host, user, password, database)

    def create(self, conn, table: str, columns: list, values: list):
        """
        データを新規作成する
        """
        query = (
            f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(values)})"
        )
        return self.execute(conn, query)

    def read(self, conn, table: str, columns: list, condition: str = None):
        """
        データを取得する
        """
        query = f"SELECT {', '.join(columns)} FROM {table}"
        if condition:
            query += f" WHERE {condition}"
        return self.execute(conn, query)

    def update(
        self, conn, table: str, columns: list, values: list, condition: str = None
    ):
        """
        データを更新する
        """
        if len(columns) != len(values):
            raise ValueError("columns と values の要素数が一致しません")

        query = f"UPDATE {table} SET "
        query += ", ".join(
            [f"{column} = {value}" for column, value in zip(columns, values)]
        )
        if condition:
            query += f" WHERE {condition}"
        return self.execute(conn, query)

    def delete(self, conn, table: str, condition: str):
        """
        データを削除する
        """
        if not condition:
            raise ValueError("condition が指定されていません")

        query = f"DELETE FROM {table} WHERE {condition}"
        return self.execute(conn, query)
