# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

from scrapy.exceptions import DropItem
from scrapy.utils.misc import load_object
from scrapy.utils.serialize import ScrapyJSONEncoder
from scrapy_redis import connection, defaults
from twisted.internet.threads import deferToThread

from adcrawler.items import AdcrawlerUrlTaskItem, AdcrawlerDataTaskItem

default_serialize = ScrapyJSONEncoder().encode


class UrlPipeline(object):
    """Pushes serialized item into a redis list/queue

    Settings
    --------
    REDIS_ITEMS_KEY : str
        Redis key where to store items.
    REDIS_ITEMS_SERIALIZER : str
        Object path to serializer function.

    """

    def __init__(self, server,
                 key=defaults.PIPELINE_KEY,
                 serialize_func=default_serialize):
        """Initialize pipeline.

        Parameters
        ----------
        server : StrictRedis
            Redis client instance.
        key : str
            Redis key where to store items.
        serialize_func : callable
            Items serializer function.

        """
        self.server = server
        self.key = key
        self.serialize = serialize_func
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_settings(cls, settings):
        params = {
            'server': connection.from_settings(settings),
        }
        if settings.get('REDIS_ITEMS_KEY'):
            params['key'] = settings['REDIS_ITEMS_KEY']
        if settings.get('REDIS_ITEMS_SERIALIZER'):
            params['serialize_func'] = load_object(
                settings['REDIS_ITEMS_SERIALIZER']
            )

        return cls(**params)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def process_item(self, item, spider):
        if not item['url']:
            raise DropItem()
        if isinstance(item, AdcrawlerUrlTaskItem):
            return deferToThread(self._process_item, item, spider.redis_key, True)
        elif isinstance(item, AdcrawlerDataTaskItem):
            return deferToThread(self._process_item, item, spider.data_key)
        else:
            self.logger.error("Unsupported item class <{}>".format(type(item)))
            raise DropItem()

    def _process_item(self, item, key, drop=False):
        serialized_task = self.serialize(item)
        # print(serialized_task)
        self.server.lpush(key, serialized_task)
        if drop:
            raise DropItem()
        return item

    def item_key(self, item, spider):
        """Returns redis key based on given spider.

        Override this function to use a different key depending on the item
        and/or spider.

        """
        return self.key % {'spider': spider.name}
