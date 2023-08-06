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
import redis
import leveldb

# self pack
from DbFactory.util.decorator import cost_time
from DbFactory.db_conf import config


class RedisSyncClient(object):
    def __init__(self, kwargs):
        self._redis_ip = kwargs.get('host', '0.0.0.0')
        self._redis_port = int(kwargs.get('port', 16379))
        self._redis_db_name = int(kwargs.get('db_name', 0))
        self._redis_passwd = kwargs.get('password')
        self._socket_timeout = kwargs.get('socket_timeout', -1)
        self._log = kwargs.get('log')

        self._retry = 10
        self._internal = 0.5  # redis 连接失败，sleep 时间
        self._cache_time = kwargs.get('cache_time', 0)
        self._leveldb_cache_dir = kwargs.get('leveldb_cache_dir')
        self._is_cache = False
        self._level_db_cache = None

        if self._cache_time > 0 and self._leveldb_cache_dir is not None:
            self._is_cache = True
            self._level_db_cache = leveldb.LevelDB(self._leveldb_cache_dir)
            self._cache_info = {}

        self.client = None
        self.connect()

    def connect(self):
        i = 0
        while self.client is None and i < self._retry:
            try:
                if self._socket_timeout <= 0:
                    self.client = redis.StrictRedis(
                        host=self._redis_ip, port=self._redis_port, db=self._redis_db_name, password=self._redis_passwd,
                        decode_responses=True
                    )
                else:
                    self.client = redis.StrictRedis(
                        host=self._redis_ip, port=self._redis_port, db=self._redis_db_name, password=self._redis_passwd,
                        decode_responses=True, socket_timeout=self._socket_timeout
                    )
            except Exception as e:
                self._log.error("redis connecting error, host: %s, port: %d, db: %s, err_msg: %s\t%s" %
                                (self._redis_ip, self._redis_port, self._redis_db_name, str(e), traceback.format_exc()))
                time.sleep(self._internal)
            i += 1
        if self.client:
            self._log.info(
                "redis connected, host: %s, port: %d, db: %s" % (self._redis_ip, self._redis_port, self._redis_db_name))
        else:
            self._log.error("last redis connecting error, host: %s, port: %d, db: %s" % (
                self._redis_ip, self._redis_port, self._redis_db_name))

    @cost_time(warning_time=config.get("REDIS_WARNING_TIME", 5))
    def get(self, *args):
        # todo 暂时没有找到优雅的方法处理这个框架，先这样吧
        try:
            res = self.client.get(*args)
        except Exception as e:
            self._log.error("redis connecting error, host: %s, port: %d, db: %s, err_msg: %s\t%s" %
                            (self._redis_ip, self._redis_port, self._redis_db_name, str(e), traceback.format_exc()))
            self.connect()
            res = self.client.get(*args)
        return res

    @cost_time(warning_time=config.get("REDIS_WARNING_TIME", 5))
    def set(self, *args):
        try:
            res = self.client.set(*args)
        except Exception as e:
            self._log.error("redis connecting error, host: %s, port: %d, db: %s, err_msg: %s\t%s" %
                            (self._redis_ip, self._redis_port, self._redis_db_name, str(e), traceback.format_exc()))
            self.connect()
            res = self.client.set(*args)
        return res

    @cost_time(warning_time=config.get("REDIS_WARNING_TIME", 5))
    def mget(self, *args):
        try:
            res = self.client.set(*args)
        except Exception as e:
            self._log.error("redis connecting error, host: %s, port: %d, db: %s, err_msg: %s\t%s" %
                            (self._redis_ip, self._redis_port, self._redis_db_name, str(e), traceback.format_exc()))
            self.connect()
            res = self.client.set(*args)
        return res

    @cost_time(warning_time=config.get("REDIS_WARNING_TIME", 5))
    def set(self, *args):
        """"""
        try:
            res = self.client.set(*args)
        except Exception as e:
            self._log.error("redis connecting error, host: %s, port: %d, db: %s, err_msg: %s\t%s" %
                            (self._redis_ip, self._redis_port, self._redis_db_name, str(e), traceback.format_exc()))
            self.connect()
            res = self.client.set(*args)
        return res

    @cost_time(warning_time=config.get("REDIS_WARNING_TIME", 5))
    def set(self, *args):
        """"""
        try:
            res = self.client.set(*args)
        except Exception as e:
            self._log.error("redis connecting error, host: %s, port: %d, db: %s, err_msg: %s\t%s" %
                            (self._redis_ip, self._redis_port, self._redis_db_name, str(e), traceback.format_exc()))
            self.connect()
            res = self.client.set(*args)
        return res

    @cost_time(warning_time=config.get("REDIS_WARNING_TIME", 5))
    def set(self, *args):
        """"""
        try:
            res = self.client.set(*args)
        except Exception as e:
            self._log.error("redis connecting error, host: %s, port: %d, db: %s, err_msg: %s\t%s" %
                            (self._redis_ip, self._redis_port, self._redis_db_name, str(e), traceback.format_exc()))
            self.connect()
            res = self.client.set(*args)
        return res

    @cost_time(warning_time=config.get("REDIS_WARNING_TIME", 5))
    def set(self, *args):
        """"""
        try:
            res = self.client.set(*args)
        except Exception as e:
            self._log.error("redis connecting error, host: %s, port: %d, db: %s, err_msg: %s\t%s" %
                            (self._redis_ip, self._redis_port, self._redis_db_name, str(e), traceback.format_exc()))
            self.connect()
            res = self.client.set(*args)
        return res

    @cost_time(warning_time=config.get("REDIS_WARNING_TIME", 5))
    def set(self, *args):
        """"""
        try:
            res = self.client.set(*args)
        except Exception as e:
            self._log.error("redis connecting error, host: %s, port: %d, db: %s, err_msg: %s\t%s" %
                            (self._redis_ip, self._redis_port, self._redis_db_name, str(e), traceback.format_exc()))
            self.connect()
            res = self.client.set(*args)
        return res

    @cost_time(warning_time=config.get("REDIS_WARNING_TIME", 5))
    def set(self, *args):
        """"""
        try:
            res = self.client.set(*args)
        except Exception as e:
            self._log.error("redis connecting error, host: %s, port: %d, db: %s, err_msg: %s\t%s" %
                            (self._redis_ip, self._redis_port, self._redis_db_name, str(e), traceback.format_exc()))
            self.connect()
            res = self.client.set(*args)
        return res

    # --------- todo 下面暂时没有使用封装 ----------
    def get_local(self, key, pos, length):
        """获取本地缓存"""
        raise AssertionError("此方法需要重写后使用")

    def put_cache_value(self, cache_key, cur_time, value):
        self._level_db_cache.Put(cache_key, json.dumps([cur_time, value]))

    def get_cache_value(self, cache_key, cur_time):
        try:
            cache_str = self._level_db_cache.Get(cache_key)
            [timestamp, cache_value] = json.loads(cache_str)
            if timestamp + self._cache_time >= cur_time:
                return cache_value
        except KeyError:
            pass
        except Exception as e:
            self._log.error("get_cache_value error, host: %s, port: %d, db: %s, err_msg: %s\t%s" % (
                self._redis_ip, self._redis_port, self._redis_db_name, str(e), traceback.format_exc()))
        raise Exception('null')

    # def get(self, key, pos, length):
    #     ret_val = []
    #     if self._is_cache:
    #         cache_key = ""
    #         cur_time = int(time.time())
    #         cache_key = "_".join([str(key), str(pos), str(length)])
    #         try:
    #             ret_val = self.get_cache_value(cache_key, cur_time)
    #             return ret_val
    #         except Exception:
    #             pass
    #     ret_val = self.get_local(key, pos, length)
    #     if self._is_cache:
    #         self.put_cache_value(cache_key, cur_time, ret_val)
    #     return ret_val

    # def get_cache_item(self, key, pos, length):
    #     cur_time = int(time.time())
    #     ret_val = None
    #     try:
    #         cache_key = "_".join([str(key), str(pos), str(length)])
    #         if self._is_cache:
    #             if self._cache_info.has_key(cache_key):
    #                 init_ts, cache_value = self._cache_info[cache_key]
    #                 if init_ts + self._cache_time >= cur_time:
    #                     ret_val = cache_value
    #         else:
    #             ret_val = self.get_local(key, pos, length)
    #             if self._is_cache:
    #                 self._cache_info[cache_key] = [cur_time, ret_val]
    #     except Exception as e:
    #         self._log.error("get_cache_item error, host: %s, port: %d, db: %s, err_msg: %s\t%s" %
    #                          (self._redis_ip, self._redis_port, self._redis_db_name, str(e), traceback.format_exc()))
    #     return ret_val

    def clear_cache(self):
        self._cache_info = {}


class RedisList(RedisClient):

    def __init__(self, redis_ip, redis_port, redis_no, redis_passwd, cache_time=0, leveldb_cache_dir=None,
                 socket_timeout=-1):
        RedisClient.__init__(self, redis_ip, redis_port, redis_no, redis_passwd, cache_time, leveldb_cache_dir,
                             socket_timeout)

    def set_local_cache_time(self, local_cache_time):
        self._is_local_cache = True
        self._local_cache_time = local_cache_time

    def get_local(self, key, pos=0, length=0, pvid=0):
        ret = []
        st = int(time.time() * 1000)
        try:
            ret = self.client.lrange(key, pos, pos + length)
        except Exception as e:
            self._log.error("get_local error, key: %s, err_msg: %s\t%s" % (str(key), str(e), traceback.format_exc()))
        et = int(time.time() * 1000)
        if et - st > 200:
            self._log.warning("get %s redis too long %s ms,redis_port:%d, host:%s, pvid:%s" % (
                key, str(et - st), self._redis_port, str(self._redis_ip), str(pvid)))
        return ret

    def set(self, key, value_list, expire_time=0, pvid=0):
        st = int(time.time() * 1000)
        tmp_key = key + str(random.randint(0, int(time.time())))
        try:
            if value_list:
                self.client.delete(key)
                len_ret = self.client.rpush(key, *value_list)
                if len_ret == len(value_list) and expire_time > 0:
                    self.client.expire(key, expire_time)
            else:
                self._log.warning("redis storing null val, key: %s, value: %s" % (key, str(value_list)))
        except Exception as e:
            self._log.error(
                "redis storing error, key: %s, err_msg: %s\t%s" % (str(key), str(e), traceback.format_exc()))
        et = int(time.time() * 1000)
        if et - st > 200:
            self._log.warning("set %s redis too long %s ms,redis_port:%d, host:%s, pvid:%s" % (
                key, str(et - st), self._redis_port, str(self._redis_ip), str(pvid)))

    def get_len(self, key):
        return self.client.llen(key)

    def lpop(self, key):
        return self.client.lpop(key)

    def rpop(self, key):
        return self.client.rpop(key)

    def lpush(self, key, value_list, timeout, pvid=0):
        st = int(time.time() * 1000)
        try:
            self.client.lpush(key, *value_list)
            if timeout > 0:
                self.client.expire(key, timeout)
        except Exception as e:
            self._log.error("lpush error, key: %s, err_msg: %s\t%s" % (str(key), str(e), traceback.format_exc()))
        et = int(time.time() * 1000)
        if et - st > 200:
            self._log.warning("lpush %s redis too long %s ms,redis_port:%d, host:%s, pvid:%s" % (
                key, str(et - st), self._redis_port, str(self._redis_ip), str(pvid)))

    def check_is_exist(self, key):
        return self.client.exists(key)


class NewRedisList(RedisClient):

    def __init__(self, redis_ip, redis_port, redis_no, redis_passwd, cache_time=0, leveldb_cache_dir=None,
                 socket_timeout=-1):
        RedisClient.__init__(self, redis_ip, redis_port, redis_no, redis_passwd, cache_time, leveldb_cache_dir,
                             socket_timeout)
        self._userid = None

    def set_userid(self, userid):
        self._userid = userid

    def set_local_cache_time(self, local_cache_time):
        self._is_local_cache = True
        self._local_cache_time = local_cache_time

    def get_local_inner(self, key, pos=0, length=0, pvid=0):
        ret = None
        st = int(time.time() * 1000)
        try:
            ret = self.client.lrange(key, pos, pos + length)
        except Exception as e:
            self._log.error("get_local error, key: %s, err_msg: %s\t%s" % (str(key), str(e), traceback.format_exc()))
        et = int(time.time() * 1000)
        if et - st > 200:
            self._log.warning("get %s redis too long %s ms,redis_port:%d, host:%s" % (
                key, str(et - st), self._redis_port, str(self._redis_ip)))
        return ret

    def get_local(self, key, pos=0, length=0, pvid=0):
        ret = None
        try:
            new_key = ''
            if self._userid is not None and self._userid.isdigit():
                if int(self._userid) % 10 == 5:
                    new_key = "QTT_" + key
            if new_key:
                ret = self.get_local_inner(new_key, pos, length)
            if ret is None:
                ret = self.get_local_inner(key, pos, length)
        except Exception as e:
            self._log.error("get_local error, key: %s, err_msg: %s\t%s" % (str(key), str(e), traceback.format_exc()))
        return ret

    def set(self, key, value_list, expire_time=0, pvid=0):
        st = int(time.time() * 1000)
        tmp_key = key + str(random.randint(0, int(time.time())))
        try:
            if value_list:
                self.client.delete(tmp_key)
                len_ret = self.client.rpush(tmp_key, *value_list)
                if len_ret == len(value_list):
                    self.client.rename(tmp_key, key)
                    if expire_time > 0:
                        self.client.expire(key, expire_time)
            else:
                self._log.warning("redis storing null val, key: %s, value: %s" % (key, str(value_list)))
        except Exception as e:
            self._log.error(
                "redis storing error, key: %s, err_msg: %s\t%s" % (str(key), str(e), traceback.format_exc()))
        et = int(time.time() * 1000)
        if et - st > 200:
            self._log.warning("set %s redis too long %s ms,redis_port:%d, host:%s" % (
                key, str(et - st), self._redis_port, str(self._redis_ip)))

    def get_len(self, key):
        return self.client.llen(key)

    def lpop(self, key):
        return self.client.lpop(key)

    def rpop(self, key):
        return self.client.rpop(key)

    def lpush(self, key, value_list, timeout, pvid=0):
        st = int(time.time() * 1000)
        try:
            self.client.lpush(key, *value_list)
            if timeout > 0:
                self.client.expire(key, timeout)
        except Exception as e:
            self._log.error("lpush error, key: %s, err_msg: %s\t%s" % (str(key), str(e), traceback.format_exc()))
        et = int(time.time() * 1000)
        if et - st > 200:
            self._log.warning("lpush %s redis too long %s ms,redis_port:%d, host:%s" % (
                key, str(et - st), self._redis_port, str(self._redis_ip)))


class RedisSortSet(RedisClient):

    def __init__(self, redis_ip, redis_port, redis_no, redis_passwd, cache_time, leveldb_cache_dir=None,
                 withscore=False, socket_timeout=-1):
        RedisClient.__init__(self, redis_ip, redis_port, redis_no, redis_passwd, cache_time, leveldb_cache_dir,
                             socket_timeout)
        self._with_score = withscore

    def get_local(self, key, pos, length):
        ret = self.client.zrevrange(key, pos, pos + length, withscores=self._with_score)
        return ret


class RedisKv(RedisClient):

    def __init__(self, redis_ip, redis_port, redis_no, redis_passwd, cache_time, leveldb_cache_dir=None,
                 socket_timeout=-1):
        RedisClient.__init__(self, redis_ip, redis_port, redis_no, redis_passwd, cache_time, leveldb_cache_dir,
                             socket_timeout)

    def get_local(self, key, pos=0, length=0, pvid=0):
        ret = []
        st = int(time.time() * 1000)
        try:
            if type(key) == list:
                if key:
                    ret = self.client.mget(key)
            else:
                ret = self.client.get(key)
        except Exception as e:
            self._log.error("get_local error, key: %s, err_msg: %s\t%s" % (str(key), str(e), traceback.format_exc()))
        et = int(time.time() * 1000)

        # self._log.warn('redis_key\t%s\t%s\t%s' % (str(type(key)),len(key),str(key)[:10]))
        if et - st > 200:
            self._log.warning("get %s redis too long %s ms,redis_port:%d, host:%s, pvid:%s" % (
                key, str(et - st), self._redis_port, str(self._redis_ip), str(pvid)))
        return ret

    def get_by_cache(self, key):
        cur_time = int(time.time())
        if type(key) == list:
            result_dict = {}
            uncache_keylist = []
            for key_item in key:
                try:
                    cache_value = self.get_cache_value(key_item, cur_time)
                    result_dict[key_item] = cache_value
                except Exception:
                    uncache_keylist.append(key_item)
            if len(uncache_keylist) > 0:
                ret = self.client.mget(uncache_keylist)
                for idx, ret_item in enumerate(ret):
                    result_dict[uncache_keylist[idx]] = ret_item
                    self.put_cache_value(uncache_keylist[idx], cur_time, ret_item)
            ret_value = [result_dict[key_item] for key_item in key]
            return ret_value
        else:
            return RedisClient.get(self, key, 0, 0)

    def set(self, key, value, timeout=0, pvid=0):
        flag = True
        st = int(time.time() * 1000)
        # tmp_key = key + str(random.randint(0, int(time.time())))
        try:
            # self.client.delete(tmp_key)
            self.client.set(key, value)
            # self.client.rename(tmp_key, key)
            if timeout > 0:
                self.client.expire(key, timeout)
        except Exception as e:
            self._log.error("set error, key: %s, err_msg: %s\t%s" % (str(key), str(e), traceback.format_exc()))
            flag = False
        et = int(time.time() * 1000)
        if et - st > 200:
            self._log.warning("set %s redis too long %s ms,redis_port:%d, host:%s, pvid:%s" % (
                key, str(et - st), self._redis_port, str(self._redis_ip), str(pvid)))
        return flag


class RedisKvZip(RedisKv):

    def set(self, key, value, timeout, pvid=0):
        st = int(time.time() * 1000)
        try:
            zlib_str = zlib.compress(value)
            RedisKv.set(self, key, zlib_str, timeout)
        except Exception as e:
            self._log.error(
                "redis storing error, key: %s, err_msg: %s\t%s" % (str(key), str(e), traceback.format_exc()))
        et = int(time.time() * 1000)
        if et - st > 200:
            self._log.warning("set %s redis too long %s ms,redis_port:%d, host:%s, pvid:%s" % (
                key, str(et - st), self._redis_port, str(self._redis_ip), str(pvid)))

    def get_local(self, key, pos=0, length=0, pvid=0):
        st = int(time.time() * 1000)
        try:
            if type(key) == list:
                ret = []
                if key:
                    ret_list = self.client.mget(key)
                    for ret_item in ret_list:
                        try:
                            if ret_item is not None:
                                ret_item_zlib = zlib.decompress(ret_item)
                                ret_item = ret_item_zlib
                        except Exception as e:
                            self._log.error("get_local error, key: %s, err_msg: %s\t%s" % (
                                str(key), str(e), traceback.format_exc()))
                        ret.append(ret_item)
            else:
                ret = self.client.get(key)
                try:
                    if ret is not None:
                        temp_st2 = int(time.time() * 1000)
                        ret = zlib.decompress(ret)
                        temp_et2 = int(time.time() * 1000)
                        if temp_et2 - temp_st2 > 200:
                            self._log.warning(
                                "get %s redis too long %s ms, zlib.decompress" % (key, str(temp_et2 - temp_st2)))
                except Exception as e:
                    self._log.error(
                        "get_local error, key: %s, err_msg: %s\t%s" % (str(key), str(e), traceback.format_exc()))
        except Exception as e:
            self._log.error("get_local error, key: %s, err_msg: %s\t%s" % (str(key), str(e), traceback.format_exc()))
            ret = None
            if type(key) == list:
                ret = [None for i in range(len(key))]
        et = int(time.time() * 1000)
        if et - st > 200:
            self._log.warning("set %s redis too long %s ms,redis_port:%d, host:%s, pvid:%s" % (
                key, str(et - st), self._redis_port, str(self._redis_ip), str(pvid)))
        return ret
