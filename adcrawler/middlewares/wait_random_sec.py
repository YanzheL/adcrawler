# -*-coding:utf-8-*-

import logging
import time
from random import *

from scrapy import signals
from scrapy.http import Request


# import scrapy.downloadermiddlewares.retry.RetryMiddleware

class WaitRandomSecMiddleware(object):
    DEFAULT_RANDOM_WAIT_INTERVAL_RANGE = 20

    def __init__(self, interval_range=DEFAULT_RANDOM_WAIT_INTERVAL_RANGE):
        self.interval_range = interval_range

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls(
            crawler.settings.get('RANDOM_WAIT_INTERVAL_RANGE', None)
        )
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        return None

    def process_response(self, request, response, spider):
        if response.status == 429:
            waitsec = randint(1, 60)
            logging.info('Spider <%s> waiting for %s seconds to continue...' % (spider.name, str(waitsec)))
            time.sleep(waitsec)
            logging.info('Spider <%s> have waited %s seconds, now retry request url <%s>' % (
                spider.name, str(waitsec), request.url))
            return Request(url=request.url, dont_filter=True)
            # return request
        else:
            return response

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
