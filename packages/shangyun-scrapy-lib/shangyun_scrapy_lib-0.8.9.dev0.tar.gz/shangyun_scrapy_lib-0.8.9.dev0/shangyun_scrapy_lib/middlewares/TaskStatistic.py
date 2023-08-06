import scrapy

from shangyun_scrapy_lib.constants import DataType
from shangyun_scrapy_lib.utils.MongoUtils import requests_statistic


# todo 可以再精细化一些，确定每个种类的任务，NewsRequest，CommentRequest
class StatisticSpiderMiddleware(object):

    # 放最后一个，就是执行成功的数量
    def process_spider_output(self, response, result, spider):
        inc_statistic("success")
        for r in result:
            if isinstance(r, scrapy.Item) or isinstance(r, dict):
                inc_statistic(r.get("media_type", False))
            yield r

    def process_spider_exception(self, response, exception, spider):
        inc_statistic("parse_error")


class StatisticDownloaderMiddleware(object):

    def process_request(self, request, spider):
        inc_statistic("request_count")
        return None

    def process_response(self, request, response, spider):
        inc_statistic("response_count")
        return response

    def process_exception(self, request, exception, spider):
        inc_statistic("download_error")


def inc_statistic(key):
    if key: return False
    requests_statistic.col.find_one_and_update(
        {"key": key}, {"$inc": {"value": 1}},
        upsert=True
    )
