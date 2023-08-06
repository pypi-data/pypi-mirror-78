# coding:utf-8
# author caturbhuja
# date   2020/8/31 5:10 下午 
# wechat chending2012 

# python pack
from functools import wraps
import time


def cost_time(log_cost_time=False, warning_time=60, log=None, request_id=''):
    """
    :param log_cost_time: 打印函数花费时间到日志
    :param warning_time: 操作耗时告警时间
    :param log: 日志 实例 接入
    :param request_id: 消息 id 用于追踪上下文日志
    :return:
    """

    def wrap(function):
        """"""
        @wraps(function)
        def cost(*args, **kwargs):
            st = int(time.time())
            res = function(*args, **kwargs)
            et = int(time.time())
            ct = et - st
            if ct >= warning_time:
                message = "request {}, Db Client Function < {} > cost too long: {}s".format(request_id,
                                                                                            function.__name__, ct)
                if log:
                    log.warning(message)
                else:
                    print(message)
            if log_cost_time:
                message = "request {}, Function < {} > cost : {}s".format(request_id, function.__name__, ct)
                if log:
                    log.warning(message)
                else:
                    print(message)
            return res
        return cost
    return wrap


def try_and_reconnect(function, reconnect_obj, log=None, request_id=''):
    """
    这个装饰器，负责尝试连接，如果报错，则重新连接，
    :param function: 函数方法
    :param reconnect_obj: 重新连接 class 的函数方法
    :param log: 日志 实例 接入
    :param request_id: 消息 id 用于追踪上下文日志
    :return:
    """
    @wraps(function)
    def cost(*args, **kwargs):
        try:
            res = function(*args, **kwargs)
        except Exception as e:
            message = "request {}, retry reconnect, error info is {}".format(request_id, e)
            if log:
                log.warning(message)
            else:
                print(message)
            res = function(*args, **kwargs)
        return res
    return cost


if __name__ == '__main__':
    @cost_time(warning_time=1)
    def test_ggg():
        time.sleep(1)


    test_ggg()
