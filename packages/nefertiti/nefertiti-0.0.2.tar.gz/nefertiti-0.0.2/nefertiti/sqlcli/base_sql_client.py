from contextlib import contextmanager


class BaseSqlClient(object):

    # 继承类必须在__init__方法中初始化self.conn
    conn = None

    def load(self, query_sql, params=None):
        with self.conn.cursor() as cur:
            cur.execute(query_sql, params)
            yield from cur

    def load_first(self, query_sql, params=None):
        with self.conn.cursor() as cur:
            cur.execute(query_sql, params)
            row = cur.fetchone()
            return row

    def save(self, merge_sql, params=None):
        cur = self.conn.cursor()
        cur.execute(merge_sql, params)
        self.conn.commit()
        cur.close()

    def __del__(self):
        self.conn.close()

    @contextmanager
    def open_transaction_cursor(self):
        cur = self.conn.cursor()
        try:
            yield cur
            self.conn.commit()
        except:
            self.conn.rollback()
        finally:
            cur.close()
