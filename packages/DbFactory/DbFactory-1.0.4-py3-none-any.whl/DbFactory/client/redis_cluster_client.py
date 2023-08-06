#!/usr/bin/env python
# -*- coding: utf-8 -*-
# wechat: chending2012

# python pack
import traceback
import time
import json
import random
import zlib

# third part pack
from rediscluster import RedisCluster   # todo  redis-3.0.1 redis-py-cluster-2.0.0 如果以前安装了redis，这个可能会导致redis 用法上有些差异
# import leveldb

# self pack
from DbFactory.client.redis_client import RedisClient
from DbFactory.util.decorator import cost_time
from DbFactory.db_conf import config


class RedisClusterClient(RedisClient):
    def __init__(self, kwargs):
        """
        _startup_nodes = [
            {"host": "10.100.16.170", "port": 6381},
            {"host": "10.100.16.170", "port": 6382},
            {"host": "10.100.16.170", "port": 6383}
        ]
        :param kwargs:
        """
        self._startup_nodes = kwargs.get('startup_nodes')
        self._redis_passwd = kwargs.get('password')
        self._decode_responses = kwargs.get('decode_responses', True)
        self._socket_timeout = kwargs.get('socket_timeout')
        self._skip_full_coverage_check = kwargs.get('skip_full_coverage_check', True)

        self._new_kwargs = dict()
        self._new_kwargs.update(
            {
                "startup_nodes": self._startup_nodes,
                "password": self._redis_passwd,
                "decode_responses": self._decode_responses,
                "socket_timeout": self._socket_timeout,
                "skip_full_coverage_check": self._skip_full_coverage_check,
            }
        )

        self._log = kwargs.get('log')

        self._retry = 10
        self._internal = 0.5  # redis 连接失败，sleep 时间

        # self._cache_time = kwargs.get('cache_time', 0)
        # self._leveldb_cache_dir = kwargs.get('leveldb_cache_dir', '.')
        # self._is_cache = False
        # self._level_db_cache = None
        #
        # if self._cache_time > 0 and self._leveldb_cache_dir is not None:
        #     self._is_cache = True
        #     self._level_db_cache = leveldb.LevelDB(self._leveldb_cache_dir)
        #     self._cache_info = {}

        self.client__ = None
        self.connect()

    def connect(self):
        i = 0
        while self.client__ is None and i < self._retry:
            try:
                self.client__ = RedisCluster(**self._new_kwargs)
            except Exception as e:
                self._log.error("redis_cluster connecting error, err_msg: %s\t%s" % (str(e), traceback.format_exc()))
                time.sleep(self._internal)
            i += 1
        if self.client__:
            self._log.info("redis_cluster connected")
        else:
            self._log.error("last redis connecting error")
