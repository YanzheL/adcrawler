from bs4 import Tag
from scrapy.utils.serialize import ScrapyJSONEncoder, ScrapyJSONDecoder

from adcrawler.scrapy_redis_bf.spiders import RedisSpider


class AdSpiderBase(RedisSpider):
    task_encoder = ScrapyJSONEncoder().encode
    task_decoder = ScrapyJSONDecoder().decode

    def next_request(self):
        serialized_task = self.server.rpop(self.redis_key)
        if serialized_task:
            self.logger.info("Got task {}".format(serialized_task))
            return self.make_request_from_task(serialized_task, callback=self.parse, dont_filter=False)

    @staticmethod
    def tagfilter(tag):
        return isinstance(tag, Tag)
