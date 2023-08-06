
class TransactionCursor(object):

    def __init__(self, sql_client):
        self.sql_client = sql_client
        self.sql_client.conn.autocommit = False
        self.cur = self.sql_client.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.rollback()
        else:
            self.commit()
        self.cur.close()

    def execute(self, sql, params):
        self.cur.execute(sql, params)

    def commit(self):
        self.sql_client.conn.commit()

    def rollback(self):
        self.sql_client.conn.rollback()

    def __del__(self):
        self.cur.close()
