import sqlite3

sqlite_db = r'.\bi_lmparts.db'

class DatabaseConnections:
    def __init__(self, sqlite_db):
        self.sqlite_db = sqlite_db
        self.sqlite_conn = None

    def connect_sqlite(self):
        try:
            self.sqlite_conn = sqlite3.connect(self.sqlite_db)
            return self.sqlite_conn
        except sqlite3.Error as e:
            print("Erro ao conectar ao SQLite:", e)
            raise

    def close_connections(self):
        if self.sqlite_conn:
            self.sqlite_conn.close()

class DataManager:
    def __init__(self, sqlite_cursor):
        self.sqlite_cursor = sqlite_cursor

    def upsert_data(self, rows, query):
        for row in rows:
            self.sqlite_cursor.execute(query, row)
        self.sqlite_cursor.connection.commit()

    def create_table(self, query):
        self.sqlite_cursor.execute(query)
