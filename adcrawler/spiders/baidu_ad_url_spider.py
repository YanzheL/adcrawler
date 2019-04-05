from bs4 import BeautifulSoup

from adcrawler.items import *
from adcrawler.spiders.ad_spider_base import AdSpiderBase


class BaiduAdUrlSpider(AdSpiderBase):
    name = 'BaiduAdUrlSpider'
    redis_key = '{}:start_urls'.format(name)
    data_key = '{}:data_urls'.format(name)

    custom_settings = {
        'ITEM_PIPELINES': {
            'adcrawler.pipelines.url_pipeline.UrlPipeline': 300
        }
    }

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        node = soup.find(name='div', attrs={'id': 'content_left'})
        adblocks = filter(self.adblockfilter, node.children)
        for adblock in adblocks:
            a_tag = adblock.find('a')
            item = AdcrawlerDataTaskItem()
            url = a_tag.attrs['href']
            item['url'] = url
            item['text'] = a_tag.text
            next_task = AdcrawlerUrlTaskItem()
            next_task['url'] = url
            next_task['cur_depth'] = response.meta['cur_depth'] + 1
            # self.logger.info(item)
            yield item
            yield next_task
            # self.try_yield(response, item)
            # self.try_yield(response, next_task)

    @staticmethod
    def adblockfilter(tag):
        if not isinstance(tag, Tag):
            return False
        class_names = tag.attrs['class']
        for cls_nm in class_names:
            if cls_nm.find('result') != -1:
                return False
        return True
