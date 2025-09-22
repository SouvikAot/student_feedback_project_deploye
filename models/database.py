import mysql.connector
from mysql.connector import Error
from config import Config
from models.exceptions import DatabaseConnectionError

class DatabaseConnection:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=Config.DB_HOST,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_NAME
            )
            self.cursor = self.conn.cursor(dictionary=True)
        except Error as e:
            raise DatabaseConnectionError(f"Could not connect to database: {e}")

    def execute(self, query, params=None):
        if not self.cursor:
            raise DatabaseConnectionError("Database not connected.")
        self.cursor.execute(query, params or ())
        return self.cursor

    def commit(self):
        if self.conn:
            self.conn.commit()

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
