from pysqlcipher3 import dbapi2 as sqlite
from fire import Fire


class Vault:
    def __init__(self, password, path="vault.db"):
        self.table = "vault"
        self.conn = sqlite.connect(path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA key='{}'".format(password))
        self.createDB()

    def createDB(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS vault (
            key TEXT NOT NULL PRIMARY KEY,
            value TEXT
            );
            """
        )

    def get(self, key, default):
        query = "select * from {table} where key='{key}'".format(
            table=self.table, key=key
        )
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result is None:
            return default
        else:
            return result[1]

    def insert(self, key, value):
        query = """
        INSERT into {table} (key, value)
        VALUES ('{key}', '{value}')
        """.format(
            table=self.table, key=key, value=value
        )
        self.cursor.execute(query)
        self.conn.commit()

    def update(self, key, value):
        query = """
        UPDATE {table}
        SET '{key}'='{value}'
        """.format(
            table=self.table, key=key, value=value
        )
        self.cursor.execute(query)
        self.conn.commit()


if __name__ == "__main__":
    Fire(Vault)
