from redis.exceptions import *
from scrapy import Request


class AdcrawlerSpiderMiddleware(object):

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        if isinstance(exception, ConnectionError):
            spider.logger.error(
                'Redis connection error when parsing url, exception <{}>, message <{}>, response url <{}>, retrying...'.format(
                    exception.__class__.__name__, exception, response.url)
            )
            return [Request(url=response.url, callback=spider.parse, dont_filter=True)]
        elif isinstance(exception, ResponseError):
            spider.logger.critical(
                '<{}> failed, exception <{}>, message <{}>, now shut down...'.format(spider.name,
                                                                                     exception.__class__.__name__,
                                                                                     exception))
            spider.crawler.engine.close_spider(spider, reason=exception)
        else:
            spider.logger.error(
                '<{}> failed, exception <{}>, message <{}>, response url <{}>, skipped this item'.format(spider.name,
                                                                                                         exception.__class__.__name__,
                                                                                                         exception,
                                                                                                         response.url))
            return []
