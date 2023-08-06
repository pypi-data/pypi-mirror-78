#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:    db_factory.py
   Description:  DB工厂类
   Author:       Caturbhuja
   date:         2020/8/31
   WeChat:       chending2012
-------------------------------------------------
   Change Activity:
       2020/8/31:   DB工厂类创建
       2020/9/1:    redis_client 方法使用反射
       2020/9/2:    DB工厂类增加自动反射

-------------------------------------------------
"""
__author__ = 'Caturbhuja'

# python pack
import os
import sys
import inspect
from functools import partial
from importlib import import_module

# self pack
from .util.six import withMetaclass
from .util.singleton import Singleton
from .db_conf import config

dir_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(dir_path)


class DbFactory(withMetaclass(Singleton)):
    """
    DbFactory DB工厂类
    利用 Singleton 控制生成db为单例模式 ，默认 每种数据库一个单例。
    通过 singleton_switch 控制是否为单例模式。

    抽象方法定义：
        详见代码

    所有方法需要相应类去具体实现：（新增数据库命名规则）
        mysql:          mysql_client.py
        mysql_pool:     mysql_pool_client.py
        redis:          redis_client.py
        redis_async:    redis_async_client.py
        redis_cluster:  redis_cluster_client.py

    数据格式例子：
        startup_nodes = [{"host": "10.100.16.170", "port": 6381},
                 {"host": "10.100.16.170", "port": 6382},
                 {"host": "10.100.16.170", "port": 6383}]

        host = '0.0.0.0'

    """

    def __init__(self, **kwargs):
        """
        :param kwargs:      其他参数
        :param db_type:     数据库类型（默认是mysql） mysql redis mysql_pool redis_cluster
        :param host:        数据库IP地址
        :param port:        端口号
        :param startup_nodes:  redis 集群 节点列表
        :param username:    账户
        :param password:    密码
        :param db_name:     数据库名称/序号
        :param singleton_switch: 单例模式开关 默认 开启
        :param singleton_num: 单例模式组别 默认 0 用于支持多个数据库连接（不用频繁切换数据库）    # todo,确定这个对所有数据库适用？
        """
        self._db_type = kwargs.get("db_type", 'mysql').upper().strip()
        self._singleton_sign = kwargs.get("singleton_sign")     # 单例标记
        self._kwargs = kwargs
        self.__init_log()
        self.__init_sub()

    def __init_log(self):
        self._log = self._kwargs.get("log")
        if not self._log:
            import logging
            logging.basicConfig(level=logging.DEBUG)
            self._log = logging

    def __init_sub(self):
        self.__parser_kwargs()
        self.__print_config()
        self.__init_db_client()
        self.atom_db = self.__get_atom_db()  # 直接暴露出 db 特殊情况下使用，如果不是封装好的orm，不推荐使用这个

    def __get_atom_db(self):
        """直接暴露出 db
        如果添加方法，按照约定，则可以不用名称。
        """
        db = self.client.client__
        return db

    def __parser_kwargs(self):
        """集中预处理kwargs中各种参数 todo ? 有必要？ """
        new_kwargs = dict()
        new_kwargs = {**self._kwargs, **new_kwargs}
        self._kwargs = new_kwargs

    def __check_client_file(self, __type):
        """
        检查数据库是否有支持文件
        """
        status = False
        for each in os.walk(dir_path):
            for name in each[2]:
                if name.endswith("py"):
                    if name.split('.')[0] == __type:
                        status = True
        if not status:
            __type = None
        assert __type, 'type error, Not support DB type: {}'.format(self._db_type)

    def __init_db_client(self):
        """
        init DB Client
        :return:
        """
        __path = "DbFactory.client.{}_client".format(self._db_type.lower())
        self.__check_client_file(__path.split('.')[-1])
        self.client = getattr(import_module(__path), self.__make_class_name())(self._kwargs)

    def __make_class_name(self):
        class_name = "{}Client".format(''.join([each.title() for each in self._db_type.split('_')]))
        return class_name

    def __print_config(self):
        """log 默认的 info debug 级别，不会打印出来"""
        self._log.info("============ DATABASE CONFIGURE =========================")
        self._log.info("DB_TYPE: %s" % self._db_type)
        self._log.info("DB_HOST: %s" % self._kwargs.get("host", "default or none"))
        self._log.info("DB_PORT: %s" % self._kwargs.get("port", "default or none"))
        self._log.info("DB_NAME: %s" % self._kwargs.get("db_name", "default or none"))
        self._log.info("DB_USER: %s" % self._kwargs.get("username", "default or none"))
        self._log.info("=========================================================")

    def __check_switch_db(self):
        if self._db_type in config.get("NO_DB_SWITCH_CLIENT"):
            raise TypeError("该数据库：{}，不支持切换db".format(self._db_type))

    # --------------------------- 自动反射 ---------------------------------
    def __getattr__(self, item):
        """如果没有遇到没有封装的命令，会自动反射"""
        return partial(self.client.generation_func, item)

    # --------------------------- 命令封装 ---------------------------------
    def switch_db(self, db_name):
        """切换db"""
        self.__check_switch_db()
        self._kwargs["db_name"] = db_name
        try:
            self.atom_db.close()
        except AttributeError:
            pass
        self.__init_sub()

    # --------------------------- 提示命令封装 -----------------------------
    def some_function(self, *args, **kwargs):
        """未来会定义的一些抽象方法"""
        return self.client.generation_func(inspect.stack()[0][3], *args, **kwargs)

    # ---------------------------- Mysql ---------------------------------
    # def select(self, *args, **kwargs):
    #     return self.client.generation_func(inspect.stack()[0][3], *args, **kwargs)
    #
    # def excute(self, *args, **kwargs):
    #     return self.client.generation_func(inspect.stack()[0][3], *args, **kwargs)

    # ---------------------------- Redis ---------------------------------
    """
    1 下列方法，原本可以使用元类自动生成。 目前这样，为了方便给用户提示，调用。
    2 如果调用方法，不在下列，会触发自动反射，完成功能。
    """
    # def get(self, *args, **kwargs):
    #     return self.client.generation_func(inspect.stack()[0][3], *args, **kwargs)
    #
    # def set(self, *args, **kwargs):
    #     return self.client.generation_func(inspect.stack()[0][3], *args, **kwargs)

    # def mget(self, *args, **kwargs):
    #     return self.client.generation_func(inspect.stack()[0][3], *args, **kwargs)
    #
    # def mset(self, *args, **kwargs):
    #     return self.client.generation_func(inspect.stack()[0][3], *args, **kwargs)
    #
    # def llen(self, *args, **kwargs):
    #     return self.client.generation_func(inspect.stack()[0][3], *args, **kwargs)
    #
    # def lpush(self, *args, **kwargs):
    #     return self.client.generation_func(inspect.stack()[0][3], *args, **kwargs)
    #
    # def rpop(self, *args, **kwargs):
    #     return self.client.generation_func(inspect.stack()[0][3], *args, **kwargs)
    #
    # def exists(self, *args, **kwargs):
    #     return self.client.generation_func(inspect.stack()[0][3], *args, **kwargs)
