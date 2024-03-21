import sqlite3

from config import DB_PATH


class Database:

    def __init__(self, file):
        self.conn = sqlite3.connect(file, check_same_thread=False)
        self.cursor = self.conn.cursor()


db = Database(DB_PATH)
