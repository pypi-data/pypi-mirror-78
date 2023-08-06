#!/usr/bin/env python
# -*- coding: utf-8 -*-
# wechat: chending2012

# python pack
import traceback
import time

# third part pack
import pymysql
import pymysql.cursors

# self pack
from DbFactory.util.decorator import cost_time
from DbFactory.db_conf import config


class MysqlClient:
    def __init__(self, kwargs):
        self.client__ = MysqlClientBase(kwargs)

    @cost_time(warning_time=config.get("MYSQL_WARNING_TIME", 5))
    def generation_func(self, method, *args, **kwargs):
        def action():
            return getattr(self.client__, method)(*args, **kwargs)

        return action()


class MysqlClientBase:
    def __init__(self, kwargs):
        self._cursor = None
        self._conn = None
        self._host = kwargs.get('host', '0.0.0.0')
        self._port = int(kwargs.get('port', 63306))
        self._user = kwargs.get('username', 'root')
        self._passwd = kwargs.get('password', 'root')
        self._db = str(kwargs.get('db_name', 'siterec_dashboard'))
        self._charset = kwargs.get('charset', 'utf8')
        self._autocommit = kwargs.get('autocommit', False)
        self._log = kwargs.get('log')
        self._new_kwargs = dict()
        self._new_kwargs.update(
            {
                "host": self._host,
                "port": self._port,
                "user": self._user,
                "passwd": self._passwd,
                "db": self._db,
                "charset": self._charset,
            }
        )
        self._retry = 10  # 重试次数
        self._internal = 1  # 重试等待时间
        self.__connect_init()

    def __connect_init(self):
        i = 0
        while self._cursor is None and i < self._retry:
            try:
                self.reconnect()
                i += 1
                if self._conn.open:
                    self._log.info("mysql connected, host: %s, port: %d, user: %s, db: %s" % (
                        self._host, self._port, self._user, self._db))
            except Exception as e:
                self._log.error("mysql connecting error, host: %s, port: %d, user: %s, db: %s, err_msg: %s\t%s" %
                                (self._host, self._port, self._user, self._db, str(e), traceback.format_exc()))

    def __del__(self):
        self.close()

    def reconnect(self):
        try:
            self.close()
            self._conn = pymysql.connect(**self._new_kwargs)
            # self.set_character_set()  todo python2 中做法，python3 中将废弃
            self._cursor = self._conn.cursor()
            if self._conn.open:
                self._log.info("mysql reconnected, host: %s, port: %d, user: %s, db: %s" % (
                    self._host, self._port, self._user, self._db))
        except Exception as e:
            time.sleep(self._internal)
            self._log.error("mysql reconnecting error, host: %s, port: %d, user: %s, db: %s, err_msg: %s\t%s" %
                            (self._host, self._port, self._user, self._db, str(e), traceback.format_exc()))

    def _select_body(self, sql, mode):
        self._cursor.execute(sql)
        if mode == "many":
            ret = self._cursor.fetchall()
        else:
            ret = self._cursor.fetchone()
        return ret

    def select(self, sql, mode="many"):
        ret = None
        try:
            if self._cursor is None:
                self.reconnect()
            ret = self._select_body(sql, mode)
        except (AttributeError, pymysql.OperationalError):
            self._log.warning("mysql not connected,  host: %s, port: %d, user: %s, db: %s, sql: %s, err_msg: %s" %
                              (self._host, self._port, self._user, self._db, sql, traceback.format_exc()))
            time.sleep(self._internal)
            self.reconnect()
            ret = self._select_body(sql, mode)
        except Exception as e:
            self._log.error("selecting error, host: %s, port: %d, user: %s, db: %s, sql: %s, err_msg: %s\t%s" %
                            (self._host, self._port, self._user, self._db, sql, str(e), traceback.format_exc()))
            # if e.args[0] == 2006:     # todo ？
            #     self.reconnect()
        return ret

    def excute(self, sql, mode="many", args=None):
        ret_status = False
        try:
            ret_status = self._excute_body(sql, mode, args)
        except (AttributeError, pymysql.OperationalError):
            self._log.warning("mysql not connected, host: %s, port: %d, user: %s, db: %s, sql: %s, err_msg: %s" %
                              (self._host, self._port, self._user, self._db, sql, traceback.format_exc()))
            time.sleep(self._internal)
            ret_status = self._excute_body(sql, mode, args)
            # count = self.cursor_.execute(sql,args)
        except Exception as e:
            self.rollback()
            self._log.error("inserting error, host: %s, port: %d, user: %s, db: %s, sql: %s, err_msg: %s\t%s" %
                            (self._host, self._port, self._user, self._db, sql, str(e), traceback.format_exc()))
            # if e.args[0] == 2006:     # todo ？
            #     self.reconnect()
        return ret_status

    def _excute_body(self, sql, mode, args):
        if self._cursor is None:
            self.reconnect()
        if mode == "many":
            self._cursor.executemany(sql, args)
        else:
            self._cursor.execute(sql, args)
        self.commit()
        ret_status = True
        return ret_status

    def autocommit(self):
        self._conn.autocommit(self._autocommit)

    def set_character_set(self):
        """
        todo 这个是python2 MysqlDb 的用法。
        :return:
        """
        self._conn.set_character_set(self._charset)

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()

    def close(self):
        try:
            if self._cursor is not None:
                self._cursor.close()
                self._cursor = None
            if self._conn is not None:
                self._conn.close()
                self._conn = None
        except Exception as e:
            self._log.error("mysql close error, host: %s, port: %d, user: %s, db: %s, err_msg: %s\t%s" %
                            (self._host, self._port, self._user, self._db, str(e), traceback.format_exc()))

    def get_rows_num(self):
        return self._cursor.rowcount

    @staticmethod
    def get_mysql_version():
        pymysql.get_client_info()
