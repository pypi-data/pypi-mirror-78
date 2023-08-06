import psycopg2
import psycopg2.extras

from nefertiti.sqlcli.base_sql_client import BaseSqlClient


class PsqlClient(BaseSqlClient):

    """
    sql语句中的params通配符使用 %s, 不用单引号包裹着
    """

    def __init__(self, database, user='postgres', password='postgres', host='localhost', port=5432, register_hstore=False):
        """Postgres Database"""
        self.conn = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
        if register_hstore:
            psycopg2.extras.register_hstore(self.conn)

    def save(self, merge_sql, params=None):
        cur = self.conn.cursor()
        cur.execute(merge_sql, params)
        if 'returning' in merge_sql:
            row = cur.fetchone()
        else:
            row = None
        self.conn.commit()
        cur.close()
        return row
