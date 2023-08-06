#!/usr/bin/env python
# -*- coding: utf-8 -*-
# wechat: chending2012

# python pack
import traceback
import time

# third part pack
import redis
# import leveldb

# self pack
from DbFactory.util.decorator import cost_time
from DbFactory.db_conf import config

"""
http://redisdoc.com/
redis 方法参考

todo 使用 leveldb 或者其他 生成本地缓存
"""


class RedisClient(object):
    def __init__(self, kwargs):
        self._redis_ip = kwargs.get('host', '0.0.0.0')
        self._redis_port = int(kwargs.get('port', 16379))
        self._redis_db_name = int(kwargs.get('db_name', 0))
        self._redis_passwd = kwargs.get('password')
        self._decode_responses = kwargs.get('decode_responses', True)
        self._socket_timeout = kwargs.get('socket_timeout')

        self._new_kwargs = dict()
        self._new_kwargs.update(
            {
                "host": self._redis_ip,
                "port": self._redis_port,
                "password": self._redis_passwd,
                "db": self._redis_db_name,
                "decode_responses": self._decode_responses,
                "socket_timeout": self._socket_timeout,
            }
        )

        self._log = kwargs.get('log')
        self._retry = 10
        self._internal = 0.5  # redis 连接失败，sleep 时间

        # self._cache_time = kwargs.get('cache_time', 0)
        # self._leveldb_cache_dir = kwargs.get('leveldb_cache_dir')
        # self._is_cache = False
        # self._level_db_cache = None
        #
        # if self._cache_time > 0 and self._leveldb_cache_dir is not None:
        #     self._is_cache = True
        #     self._level_db_cache = leveldb.LevelDB(self._leveldb_cache_dir)
        #     self._cache_info = {}

        self.client__ = None  # 统一规定 数据库实例使用这个名字

        self.connect()

    def connect(self):
        i = 0
        while self.client__ is None and i < self._retry:
            try:
                self.client__ = redis.StrictRedis(**self._new_kwargs)
            except Exception as e:
                self._log.error("redis connecting error, host: %s, port: %d, db: %s, err_msg: %s\t%s" %
                                (self._redis_ip, self._redis_port, self._redis_db_name, str(e), traceback.format_exc()))
                time.sleep(self._internal)
            i += 1
        if self.client__:
            self._log.info(
                "redis connected, host: %s, port: %d, db: %s" % (self._redis_ip, self._redis_port, self._redis_db_name))
        else:
            self._log.error("last redis connecting error, host: %s, port: %d, db: %s" % (
                self._redis_ip, self._redis_port, self._redis_db_name))

    def _try_and_reconnect(self, function):
        try:
            res = function()
        except Exception as e:
            self._log.error("redis connecting error, err_msg: %s\t%s" % (str(e), traceback.format_exc()))
            self.connect()
            res = function()
        return res

    @cost_time(warning_time=config.get("REDIS_WARNING_TIME", 5))
    def generation_func(self, method, *args, **kwargs):
        def action():
            return getattr(self.client__, method)(*args, **kwargs)

        return self._try_and_reconnect(action)
