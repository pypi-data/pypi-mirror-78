[TOC]

介绍
~~~~

数据库模块：集成我们日常使用数据库，将包含如下内容：redis（同步，异步，集群），mysql（同步，异步，集群），elastic\_search（同步集群，异步集群）

目前实现：DbFactory框架，redis 同步连接，mysql 同步连接 功能

为什么需要这个模块：

::

    1. 这个模块里面封装了工程过程中经常遇到的问题的自动解决方案，提高系统稳定性。
    2. 可能，方便大家操作叭。  
    3. 可能，用起来有点爽叭。

好的功能
~~~~~~~~

::

    1. 非常方便的实例化数据库连接类
    2. 自动单例模式，以及单例控制
    3. 新增 慢查询 告警 功能：查询超过设定时间，会在日志中告警
    4. 支持 request_id 写入日志，方便 debug 时查找上下文
    5. 支持 数据库连接 异常 重连机制
    6. 方便开发，拓展新数据库客户端非常简单

使用方法
~~~~~~~~

详见：db\_demo.py 部分案例：

.. code:: python

    import logging

    logging.basicConfig(level=logging.DEBUG)
    logging.info('nice')

    from DbFactory import DbFactory

    # ----------- 创建 mysql 数据库 ------------
    mysql_client = DbFactory(log=logging, db_type="mysql", port=53307, password='123456',
                             db_name='database_name')  # 如果未选择参数，则使用默认。db_type 默认 mysql

    print("_singleton_sign:", mysql_client._singleton_sign)     # 显示单例名称
    print(mysql_client.select("select * from appinfo"))     # 调用 select 方法

    mysql_client.switch_db("database_name_2")      # 切换数据库 
    print(mysql_client.select("select * from appinfo"))   # 调用 select 方法

    # 如果一次连接多个数据库，也可以采用多个单例的方式。
    # ---------------- 多个单例 -----------------
    mysql_client1 = DbFactory(log=logging, db_type="mysql", port=53307, password='123456',
                             db_name='database_name')  # 如果未选择参数，则使用默认。db_type 默认 mysql
    print("_singleton_sign1:", mysql_client1._singleton_sign)

    mysql_client2 = DbFactory(log=logging, db_type="mysql", port=53307, password='123456',
                             db_name='database_name', singleton_num=2)  # 如果未选择参数，则使用默认。db_type 默认 mysql
    print("_singleton_sign2:", mysql_client2._singleton_sign)

    # ----------- 创建 mysql 数据库 连接池方式 ------------
    # 待完善
    # mysql_pool_client = DbFactory(log=logging)
    # print(mysql_client.client.select("select * from pangu_synonyms_words"))

    # ----------- 创建 sql achemy 数据库 ------------
    # 待完善
    # mysql_client = DbFactory(log=logging, db_type="mysql", port=53307, password='123456',
    #                         db_name='oppo')  # 如果未选择参数，则使用默认。db_type 默认 mysql
    # print(mysql_client.select("select * from appinfo"))

    # ----------- 创建 redis 数据库 ------------
    redis_client = DbFactory(log=logging, db_type="redis", port=16379, password='123456')
    redis_client.set("nice", "友友快@我！")      # 调用set方法
    print(redis_client.get("nice"))     # 调用get方法

    redis_client.switch_db(1)      # 切换数据库
    redis_client.set("nice", "友友快切换！")
    print(redis_client.get("nice"))

    # ----------- 创建 redis cluster 数据库 ------------
    startup_nodes = [{"host": "10.100.16.170", "port": 6381},
                     {"host": "10.100.16.170", "port": 6382},
                     {"host": "10.100.16.170", "port": 6383}]
    redis_cluster_client = DbFactory(log=logging, db_type="redis_cluster", startup_nodes=startup_nodes, password='123456')
    redis_cluster_client.set("nice", "友友集群快@我！")
    print(redis_cluster_client.get("nice"))

    # ----------- 特殊情况，直接使用 原始的db，不推荐。（现成封装好的ORM除外，例如 sqlachemy） ------------
    print(mysql_client.atom_db.select("select * from appinfo"))
    print(redis_client.atom_db.get("nice"))
    print(redis_cluster_client.atom_db.get("nice"))

参数说明
~~~~~~~~

详见：db\_client.py

开发方法
~~~~~~~~

所有方法需要相应类去具体实现：（新增数据库命名规则）

::

    mysql:          mysql_client.py
    mysql_pool:     mysql_pool_client.py
    redis:          redis_client.py
    redis_async:    redis_async_client.py
    redis_cluster:  redis_cluster_client.py

新增新的数据库时，例子如下：（拿 redis\_cluster 为例子）

1. 调用名称 redis\_cluster ，用在创建数据库时，db\_type 参数
2. DbFactory/client 文件夹内部，新建 redis\_cluster\_client.py 文件。
3. 新建类名 RedisClusterClient
4. 类内部 约定实现如下方法： （具体可以参考 redis\_client.py
   以及，mysql\_client.py）

.. code:: python

    # 这个方法建立反射，DbFactory 类能够直接调用到 RedisClusterClient 类中 封装的方法。
    @cost_time(warning_time=config.get("REDIS_WARNING_TIME", 5))
    def generation_func(self, method, *args, **kwargs):
        def action():
            return getattr(self.client__, method)(*args, **kwargs)
        return action()

注意事项
~~~~~~~~

1. 部分方法，不太常见，所以未封装提示功能，但不影响使用，如果需要，可以自行添加提示。

依赖列表以及部分版本信息
~~~~~~~~~~~~~~~~~~~~~~~~

::

    redis 3.3.11   
    redis 集群  
    aredis （异步模块）1.1.7  
    pymysql     0.9.3  
    SQLAlchemy (以及封装文件)  
    marshell 序列化，反序列化  
    elasticsearch   （同步）  
    elasticsearch_async     (异步)  

todo
~~~~

| 考虑，flask 集成？
| 考虑，tornado 集成？
| todo 注意，单例模式，在 tornado 多线程模式下，可能失效？
找机会探究下。

更新日志
~~~~~~~~

::

    Change Activity:  
       2020/8/31:   DB工厂类创建  
       2020/9/1:    redis_client 方法使用反射  
       2020/9/2:    DB工厂类增加自动反射
