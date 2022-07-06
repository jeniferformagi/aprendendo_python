import psycopg2 as database


class Connection():
    def __init__(self):
        self.cnx = database.connect(
            host="172.28.1.4",
            database="postgres",
            user="postgres",
            password="postgres"
        )
        self.cur = self.cnx.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.cnx.close()

    def commit(self):
        self.cnx.commit()

    def close(self):
        self.cur.close()
        self.cnx.close()

    def fetchall(self):
        return self.cur.fetchall()

    def execute(self, sql, params=None):
        self.cur.execute(sql, params or ())

    def query(self, sql, params=None):
        self.execute(sql, params)
        return self.fetchall()

        