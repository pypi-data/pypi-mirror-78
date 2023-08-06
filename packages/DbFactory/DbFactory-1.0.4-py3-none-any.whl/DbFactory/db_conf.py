# coding:utf-8
# author caturbhuja
# date   2020/9/1 3:15 下午 
# wechat chending2012 

config = {
    # 数据库执行时间，超时告警。     # todo 后续支持多级别告警
    "MYSQL_WARNING_TIME": 5,
    "REDIS_WARNING_TIME": 30,

    # 数据库连接重试时间

    "NO_DB_SWITCH_CLIENT": ["redis_cluster"]    # 不支持 切换db 的数据库
}



