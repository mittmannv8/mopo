import sqlite3

class Database(object):
    """Database connection.

    For now, only SQLite3 is supported."""

    def __init__(self, db_name):
        self.db_name = db_name
        self.connect()

    def connect(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def create_table(self, model):
        cur = self.cursor
        model = model()

        print(model.nome)

