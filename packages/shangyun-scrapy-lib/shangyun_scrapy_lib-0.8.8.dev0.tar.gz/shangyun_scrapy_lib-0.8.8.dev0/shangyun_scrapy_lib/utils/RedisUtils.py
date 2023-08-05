import os

import redis


class RedisQueue():
    def __init__(self):
        self._name = "screen_urls"
        self._url = os.environ.get("REDIS_SCREENSHOT_QUEUE")
        self._client = redis.Redis.from_url(self._url)

    def push(self, url, data_id):
        if not (url or data_id):
            return False
        value = f"{data_id},{url}"
        return self._client.lpush(self._name, value)