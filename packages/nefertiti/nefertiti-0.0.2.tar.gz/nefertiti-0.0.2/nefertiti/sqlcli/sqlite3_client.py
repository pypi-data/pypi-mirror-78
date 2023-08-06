import sqlite3

from nefertiti.sqlcli.base_sql_client import BaseSqlClient


class Sqlite3Client(BaseSqlClient):

    """
    原生sql语句里面的params通配符使用 ?
    sqlite多conn写的时候会出现lock问题, 可以一个进程只创建一个conn
    """

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
