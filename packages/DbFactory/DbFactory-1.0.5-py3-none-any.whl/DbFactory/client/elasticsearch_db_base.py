# -*- coding:utf-8 -*-
import time
import elasticsearch
import requests
import json
import random

from conf.environment import config

from logger import log

# todo 卧槽，这个有问题，同样的语句，kibana有结果，这个没有结果！！！
# class ElasticSearchBase(object):
#     def __init__(self, servers_addr: list):
#         self.servers_addr = servers_addr
#         try:
#             self.es_client = elasticsearch.Elasticsearch(servers_addr)
#         except Exception as exc:
#             log.error("failed to connect to elasticsearch servers %s" % exc)
#
#     def search(self, index, body):
#         retry_times = 3
#         while retry_times > 0:
#             try:
#                 result = self.es_client.search(index, body)
#                 return result
#             except Exception as exc:
#                 time.sleep(5)
#                 log.error("failed to connect to elasticsearch servers %s" % exc)
#                 self.reconnect()
#                 retry_times -= 1
#         return dict()
#
#     def reconnect(self):
#         self.es_client = elasticsearch.Elasticsearch(self.servers_addr)


class ElasticSearchBase(object):
    def __init__(self, servers_addr: list):
        self._servers_addr = servers_addr

    def search(self, index, body):
        url = random.choice(self._servers_addr)
        # if url[-1] == '/':
        #     url.pop(-1)   # todo 自动处理下 网址分隔符
        whole_url = "{}{}/_search".format(url, index)
        return self._action_search(whole_url, body)

    def mapping(self, index):
        url = random.choice(self._servers_addr)
        # if url[-1] == '/':
        #     url.pop(-1)   # todo 自动处理下 网址分隔符
        whole_url = "{}{}/_mapping".format(url, index)
        body = None
        return self._action_search(whole_url, body)

    def indices(self):
        url = random.choice(self._servers_addr)
        # if url[-1] == '/':
        #     url.pop(-1)   # todo 自动处理下 网址分隔符
        whole_url = "{}_cat/indices".format(url)
        # print("whole_url:{}".format(whole_url))
        
        return self._action_search(whole_url)

    def _action_search(self, whole_url, body=None):
        retry_times = 3
        ret_mark = config.RETURN_CODE_FAILED
        error_reason = ''
        while retry_times > 0:
            try:
                request_id = int(time.time())
                ret_mark, ret_value, error_reason = self._get_http_response(whole_url, body, request_id)
                return ret_mark, ret_value, error_reason
            except Exception as exc:
                time.sleep(5)
                log.error("failed to connect to elasticsearch servers %s" % exc)
                retry_times -= 1
        return ret_mark, dict(), error_reason

    @staticmethod
    def _get_http_response(url, params, request_id):
        ret_mark = config.RETURN_CODE_SUCCESS
        ret_value = {}
        error_reason = ""
        start_time = time.time()
        headers = {
            "Content-Type": "application/json"
        }
        try:
            if params:
                response = requests.post(url, data=json.dumps(params), headers=headers, timeout=config.REQUEST_TIMEOUT)
            else:
                response = requests.get(url, headers=headers, timeout=config.REQUEST_TIMEOUT)
            if response.status_code != 200:
                ret_mark = config.RETURN_CODE_FAILED
                error_reason = "search internal error"
                log.error("request: %s\terror: %s" % (url, response.text))
                return ret_mark, ret_value, error_reason
            ret_value = json.loads(response.text)
            if "error" in ret_value:
                ret_mark = config.RETURN_CODE_FAILED
                error_reason = "search internal error"
                log.error("request: %s\terror: %s" % (url, str(ret_value["error"])))
                return ret_mark, ret_value, error_reason
        except requests.exceptions.Timeout:
            ret_mark = config.RETURN_CODE_TIME_OUT
            error_reason = "search time out"
            log.warn("request time out: %s" % url)
            return ret_mark, ret_value, error_reason
        except Exception as e:
            ret_mark = config.RETURN_CODE_FAILED
            error_reason = "search internal error"
            log.error("request: %s\terror: %s" % (url, str(e)))
            return ret_mark, ret_value, error_reason
        end_time = time.time()
        duration = end_time - start_time
        log.info(
            "elasticsearch latency = " + str(duration) + " url = " + url + " request_id = " + str(request_id))
        return ret_mark, ret_value, error_reason
