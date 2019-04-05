# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AdcrawlerUrlTaskItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    cur_depth = scrapy.Field()


class AdcrawlerDataTaskItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    fingerprint = scrapy.Field()
    ad_img_urls = scrapy.Field()


class AdcrawlerDataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    fingerprint = scrapy.Field()
    ad_img_urls = scrapy.Field()
    screenshot_filename = scrapy.Field()
    ad_img_paths = scrapy.Field()
