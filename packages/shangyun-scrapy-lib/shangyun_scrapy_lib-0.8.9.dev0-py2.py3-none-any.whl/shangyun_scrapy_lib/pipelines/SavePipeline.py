import os

from shangyun_scrapy_lib.BaseItems.base_item import BaseItem
from shangyun_scrapy_lib.constants import DataType
from shangyun_scrapy_lib.constants.DictKey import DATA_ID
from shangyun_scrapy_lib.utils.MongoUtils import comment_result, news_result, tieba_comment_result, tieba_post_result
from shangyun_scrapy_lib.utils.RedisUtils import RedisQueue
from shangyun_scrapy_lib.utils.TimeUtils import now


class SavePipeline(object):
    def __init__(self):
        self.comment_col = comment_result.col
        self.news_col = news_result.col
        self.tieba_comment_col = tieba_comment_result.col
        self.tieba_post_col = tieba_post_result.col
        self.task_id = os.environ.get('CRAWLAB_TASK_ID')

        self.queue = RedisQueue()
        self.type2col = {
            DataType.NEWS: self.news_col,
            DataType.TOUTIAO: self.news_col,
            DataType.COMMENT: self.comment_col,
            DataType.TIEBA: self.tieba_post_col,
            DataType.TIEBA_COMMENT: self.tieba_comment_col
        }

    def process_item(self, item: BaseItem, spider):
        # 转成item
        save_item = dict(item)
        # 设置taskid
        save_item['task_id'] = self.task_id

        col = self.type2col[save_item["media_type"]]
        # 查询原始数据
        data = col.find_one({"data_id": save_item[DATA_ID]})
        if data:
            save_item["insert_time"] = data['insert_time']
            save_item["task_id"] = data['task_id']
            col.update_one({"data_id": save_item[DATA_ID]},
                           {"$set": save_item},
                           upsert=True)
        else:
            save_item["insert_time"] = now()
            if "NewsItem" in str(item.__class__):
                # 新闻类型的item，全部截图
                self.queue.push(save_item["url"], save_item["data_id"])
            col.insert_one(save_item)
        return save_item
