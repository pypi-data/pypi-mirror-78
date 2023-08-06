#!/usr/bin/env python
# -*- coding: utf-8 -*-
from stat_driver import *


class ConnectionPool:
    _pool = None

    def __enter__(self):
        self.conn = self.__get_conn()
        self.cursor = self.conn.cursor()

    def __get_conn(self):
        config = {
            "host": conf.MYSQL_URL,
            "port": conf.MYSQL_PORT,
            "database": conf.MYSQL_DASHBOARD_DB,
            "user": conf.MYSQL_USER,
            "password": conf.MYSQL_PASSWD,
            "charset": conf.MYSQL_CHARSET,
        }

        if self._pool is None:
            self._pool = PooledDB(
                creator=pymysql,
                maxconnections=conf.MYSQL_MAX_CONNECTIONS,
                mincached=conf.MYSQL_MIN_CACHED,
                maxcached=conf.MYSQL_MAX_CACHED,
                maxshared=conf.MYSQL_MAC_SHARED,
                blocking=conf.MYSQL_BLOCKING,
                setsession=conf.MYSQL_SET_SESSION,
                ping=1,
                **config,
            )
        return self._pool.connection()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()

    def get_conn(self):
        conn = self.__get_conn()
        cursor = conn.cursor()
        return conn, cursor


def get_connection_pool():
    return ConnectionPool()


class MySQLClient:

    def __init__(self):
        self.pool = get_connection_pool()
        self._interval = 5

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(MySQLClient, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def select(self, sql, mode="many"):
        ret = ()
        conn, cursor = None, None
        retry, ret_status = 5, False
        while retry >= 0:
            try:
                conn, cursor, count = self.execute(sql, mode="one", auto_close=False)
                if mode == "many":
                    ret = cursor.fetchall()
                else:
                    ret = cursor.fetchone()
                self.close(conn, cursor)
                ret_status = True
                return ret
            except Exception as e:
                err_msg = traceback.format_exc().replace("\n", "")
                ilog_warn.warning(f"select failure retry: {retry}, sql: {sql}, err_msg: {str(e)}\t{err_msg}")
                self.close(conn, cursor)
                retry -= 1

        if not ret_status:
            ilog.error(f"select error, sql: {sql}")

        return ret

    def execute(self, sql, mode="many", args=None, auto_close=True):
        retry = 1
        conn, cursor = None, None
        count = -1
        while retry >= 0:
            try:
                conn, cursor = self.pool.get_conn()
                if mode == "many":
                    cursor.executemany(sql, args)
                else:
                    count = cursor.execute(sql, args)
                count = cursor.rowcount
                conn.commit()
                if auto_close:
                    self.close(conn, cursor)
                break
            except (AttributeError, pymysql.err.OperationalError) as e:
                self.close(conn, cursor)
                err_msg = traceback.format_exc().replace("\n", "")
                ilog_warn.warning(f"mysql connect error, err_msg: {str(e)}\t{err_msg}")
                retry -= 1
                time.sleep(self._interval)
            except Exception as e:
                if conn:
                    conn.rollback()
                self.close(conn, cursor)
                err_msg = traceback.format_exc().replace("\n", "")
                ilog.error(f"execute error, sql: {sql}, err_msg: {str(e)}\t{err_msg}")
        return conn, cursor, count

    @staticmethod
    def close(conn, cursor):
        try:
            if conn:
                conn.close()
            if cursor:
                cursor.close()
        except Exception as e:
            err_msg = traceback.format_exc().replace("\n", "")
            ilog.error(f"mysql close error, err_msg: {str(e)}\t{err_msg}")


def main():
    mysql_client = MySQLClient()
    # sql = "select appid from pangu_app_info where is_online = 1"
    # results = mysql_client.execute(sql, mode="one")
    # print(results)
    # sql = f'delete from pangu_statistic_total_puv where appid = "199606" and data_time = "2020.08.13"'
    # results = mysql_client.execute(sql, "one")
    # print(results)


if __name__ == '__main__':
    main()
