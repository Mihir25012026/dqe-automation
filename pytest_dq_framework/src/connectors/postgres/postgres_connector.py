import psycopg2
import pandas as pd


class PostgresConnectorContextManager:

    def __init__(self, db_host, db_name, db_port, db_user, db_password):
        self.db_host = db_host
        self.db_name = db_name
        self.db_port = db_port
        self.db_user = db_user
        self.db_password = db_password
        self.connection = None

    def __enter__(self):
        try:
            self.connection = psycopg2.connect(
                host=self.db_host,
                database=self.db_name,
                port=self.db_port,
                user=self.db_user,
                password=self.db_password
            )
            return self
        except Exception as e:
            raise Exception(f"DB connection failed: {e}")

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.connection:
            self.connection.close()

    def get_data_sql(self, sql):
        try:
            df = pd.read_sql(sql, self.connection)
            return df
        except Exception as e:
            raise Exception(f"Query execution failed: {e}")