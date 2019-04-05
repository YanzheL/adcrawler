from scrapy.http import Request
from scrapy.utils.serialize import ScrapyJSONEncoder, ScrapyJSONDecoder

from adcrawler.items import AdcrawlerDataItem
from adcrawler.scrapy_redis_bf.dupefilter import RFPDupeFilter
from adcrawler.scrapy_redis_bf.spiders import RedisSpider


class AdDataSpider(RedisSpider):
    name = 'AdDataSpider'
    redis_key = 'data_tasks'
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy.pipelines.images.ImagesPipeline': 302,
            'adcrawler.pipelines.mongo.MongoPipeline': 303
        }
    }

    _filter = None
    task_encoder = ScrapyJSONEncoder().encode
    task_decoder = ScrapyJSONDecoder().decode

    @property
    def filter(self):
        if not self._filter:
            self._filter = RFPDupeFilter(self.server, self.settings.get('DUPEFILTER_KEY', '%(spider)s:dupefilter'))
        return self._filter

    def next_request(self):
        serialized_task = self.server.rpop(self.redis_key)
        if serialized_task:
            self.logger.info("Got task {}".format(serialized_task))
            return self.make_request_from_task(serialized_task, callback=self.parse, dont_filter=False)

    def parse(self, response):
        yield AdcrawlerDataItem(response.request.meta['task'])

    def make_request_from_task(self, serialized_task, **kwargs):
        serialized_task = str(serialized_task, 'utf8')
        task = self.task_decoder(serialized_task)
        request = Request(
            url=task['url'],
            **kwargs
        )
        request.meta['task'] = dict(task)
        return request
