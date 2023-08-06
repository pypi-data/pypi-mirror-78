import pymssql

from nefertiti.sqlcli.base_sql_client import BaseSqlClient


class MssqlClient(BaseSqlClient):

    """
    原生sql语句中的param通配符使用 %s, 不加引号
    """

    def __init__(self, database, user, password, host, port=1433):
        """SQL Server Database"""
        self.conn = pymssql.connect(server=host, user=user, password=password, database=database, port=port)

    def load(self, query_sql, params=None):
        # 同一个conn同时执行多个load语句时, 后执行的污染之前执行的. 故不能使用yield方式
        return list(super(MssqlClient, self).load(query_sql, params))
