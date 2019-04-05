from scrapy.http import Request

from adcrawler.items import AdcrawlerDataItem
from adcrawler.spiders.ad_spider_base import AdSpiderBase


class AdDataSpider(AdSpiderBase):
    name = 'AdDataSpider'
    redis_key = 'data_tasks'
    custom_settings = {
        'ITEM_PIPELINES': {
            'adcrawler.pipelines.screenshot.ScreenshotPipeline': 301,
            'scrapy.pipelines.images.ImagesPipeline': 302,
            'adcrawler.pipelines.mongo.MongoPipeline': 303
        }
    }

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
