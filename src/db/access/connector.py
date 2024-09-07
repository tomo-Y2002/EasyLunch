import mysql.connector
from google.cloud.logging import Client

logging_client = Client()
logger = logging_client.logger("easylunch")


class MySQLConnector:
    """
    MySQL のサーバに接続するクラス
    """

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = 3306
        logger.log_text(
            f"host: {host}, user: {user}, database: {database}, password: {password}"
        )
        logger.log_text(
            f"type(host): {type(host)}, type(user): {type(user)}, type(database): {type(database)}, type(password): {type(password)}"
        )

    def connect(self):
        """
        データベースへの接続を行う
        """
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
            )
            return conn
        except mysql.connector.Error as e:
            print(f"Error connecting to MySQL Platform: {e}")
            logger.log_text(f"Error connecting to MySQL Platform: {e}")
            return None

    def close(self, conn):
        """
        データベースへの接続を閉じる
        """
        try:
            conn.close()
        except mysql.connector.Error as e:
            print(f"Error closing MySQL connection: {e}")
            logger.log_text(f"Error closing MySQL connection: {e}")

    def commit(self, conn):
        """
        トランザクションをコミットする
        """
        try:
            conn.commit()
        except mysql.connector.Error as e:
            print(f"Error committing transaction: {e}")
            logger.log_text(f"Error committing transaction: {e}")

    def execute(self, conn, query):
        """
        クエリを実行する
        """
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except mysql.connector.Error as e:
            print(f"Error executing query: {e}")
            logger.log_text(f"Error executing query: {e}")
            return None


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
        try:
            query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(values)})"
            return self.execute(conn, query)
        except mysql.connector.Error as e:
            print(f"Error creating data: {e}")
            logger.log_text(f"Error creating data: {e}")
            return None

    def read(self, conn, table: str, columns: list, condition: str = None):
        """
        データを取得する
        """
        try:
            query = f"SELECT {', '.join(columns)} FROM {table}"
            if condition:
                query += f" WHERE {condition}"
            return self.execute(conn, query)
        except mysql.connector.Error as e:
            print(f"Error reading data: {e}")
            logger.log_text(f"Error reading data: {e}")
            return None

    def update(
        self, conn, table: str, columns: list, values: list, condition: str = None
    ):
        """
        データを更新する
        """
        try:
            if len(columns) != len(values):
                raise ValueError("columns と values の要素数が一致しません")

            query = f"UPDATE {table} SET "
            query += ", ".join(
                [f"{column} = {value}" for column, value in zip(columns, values)]
            )
            if condition:
                query += f" WHERE {condition}"
            return self.execute(conn, query)
        except mysql.connector.Error as e:
            print(f"Error updating data: {e}")
            logger.log_text(f"Error updating data: {e}")
            return None

    def delete(self, conn, table: str, condition: str):
        """
        データを削除する
        """
        try:
            if not condition:
                raise ValueError("condition が指定されていません")

            query = f"DELETE FROM {table} WHERE {condition}"
            return self.execute(conn, query)
        except mysql.connector.Error as e:
            print(f"Error deleting data: {e}")
            logger.log_text(f"Error deleting data: {e}")
            return None
