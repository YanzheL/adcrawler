from collections.abc import Iterable

from bs4 import Tag, BeautifulSoup
from scrapy.http import Request
from scrapy.utils.request import request_fingerprint

from adcrawler.items import AdcrawlerDataTaskItem, AdcrawlerUrlTaskItem
from adcrawler.spiders.ad_spider_base import AdSpiderBase
from adcrawler.utils.links_process import fix_url


class AdUrlSpider(AdSpiderBase):
    name = 'AdUrlSpider'
    redis_key = '{}:url_tasks'.format(name)
    data_key = 'data_tasks'.format(name)
    custom_settings = {
        'ITEM_PIPELINES': {
            'adcrawler.pipelines.url_task.UrlPipeline': 300,
        }
    }
    MAX_URL_TASKS = 10000

    def make_request_from_task(self, serialized_task, **kwargs):
        serialized_task = str(serialized_task, 'utf8')
        task = self.task_decoder(serialized_task)
        request = Request(
            url=task['url'],
            **kwargs
        )
        request.meta['cur_depth'] = task['cur_depth']
        request.meta['splash'] = {
            'args': {
                # set rendering arguments here
                'html': 1,
                'wait': 10
                # 'png': 1,

                # 'url' is prefilled from request url
                # 'http_method' is set to 'POST' for POST requests
                # 'body' is set to request body for POST requests
            },
            # optional parameters
            'endpoint': 'render.html',  # optional; default is render.json
            # 'splash_url': '<url>',  # optional; overrides SPLASH_URL
            # 'slot_policy': scrapy_splash.SlotPolicy.PER_DOMAIN,
            # 'splash_headers': {},  # optional; a dict with headers sent to Splash
            'dont_process_response': False,  # optional, default is False
            'dont_send_headers': False,  # optional, default is False
            'magic_response': True,  # optional, default is True
        }
        return request

    def parse(self, response):
        self.logger.info("Parse")
        soup = BeautifulSoup(response.body, 'lxml')
        all_img_tags = filter(self.tagfilter, soup.find_all('img'))
        candidate_img_tags = filter(lambda o: self.has_ad(o) or self.sibling_has_ad(o), all_img_tags)
        for candidate in candidate_img_tags:
            ad_url = self.get_img_ad_url(candidate)
            ad_src = candidate.attrs.get('src', None)
            ad_url = fix_url(ad_url)
            ad_src = fix_url(ad_src)
            if not ad_url or not ad_src:
                continue
            item = AdcrawlerDataTaskItem()
            item['url'] = ad_url
            item['fingerprint'] = request_fingerprint(response.request)
            item['ad_img_urls'] = [ad_src]
            yield item
        all_a_tags = soup.find_all('a')
        if self.server.llen(self.redis_key) > self.MAX_URL_TASKS:
            return
        for at in all_a_tags:
            a_url = at.attrs.get('href', None)
            a_url = fix_url(a_url)
            if not a_url:
                continue
            next_task = AdcrawlerUrlTaskItem()
            next_task['url'] = a_url
            next_task['cur_depth'] = response.meta['cur_depth'] + 1
            yield next_task

    @staticmethod
    def get_best_a_tag(a_tags):
        tag = None
        href = None
        for a_tag in a_tags:
            if 'href' not in a_tag.attrs:
                continue
            if tag is None or len(a_tag.attrs['href']) > len(tag.attrs['href']):
                tag = a_tag
                href = a_tag.attrs['href']
        return tag, href

    @staticmethod
    def get_img_ad_url(img_tag):
        if not isinstance(img_tag, Tag):
            return
        if 'data-url' in img_tag.attrs:
            url = img_tag.attrs['data-url']
            return url
        parent = img_tag.parent
        if parent.name == 'a' and 'href' in parent.attrs:
            return parent.attrs['href']
        sibling_a_tags = parent.find_all("a", recursive=False)
        best_a, best_href = AdUrlSpider.get_best_a_tag(sibling_a_tags)
        return best_href

    @staticmethod
    def has_ad(element):
        if element is None:
            return False
        finder = lambda s: isinstance(s, str) and s.find('广告') != -1
        if isinstance(element, Tag):
            for v in element.attrs.values():
                if isinstance(v, Iterable):
                    for i in v:
                        if finder(i):
                            return True
                elif finder(v):
                    return True
            if element.string and finder(element.string):
                return True
        elif finder(element):
            return True
        return False

    @staticmethod
    def sibling_has_ad(element):
        if element is None:
            return False
        parent = element.parent
        children = parent.children
        for child in children:
            if AdUrlSpider.has_ad(child):
                return True
