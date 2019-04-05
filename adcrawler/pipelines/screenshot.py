import os
from hashlib import sha1

import scrapy


class ScreenshotPipeline(object):
    """Pipeline that uses Splash to render screenshot of
    every Scrapy item."""

    def __init__(self, screenshot_dir, max_retry=10):
        self.screenshot_dir = screenshot_dir
        self.max_retry = max_retry
        os.makedirs(self.screenshot_dir, exist_ok=True)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            crawler.settings['SCREENSHOT_DIR'],
            crawler.settings['RETRY_TIMES']
        )

    def process_item(self, item, spider):
        request = scrapy.Request(item["url"])
        request.meta['splash'] = {
            'args': {
                # set rendering arguments here
                'html': 0,
                'width': 600,
                'render_all': 1,
                'wait': 20
                # 'url' is prefilled from request url
                # 'http_method' is set to 'POST' for POST requests
                # 'body' is set to request body for POST requests
            },

            # optional parameters
            'endpoint': 'render.png',  # optional; default is render.json
            # 'splash_url': '<url>',  # optional; overrides SPLASH_URL
            # 'slot_policy': scrapy_splash.SlotPolicy.PER_DOMAIN,
            # 'splash_headers': {},  # optional; a dict with headers sent to Splash
            # 'dont_process_response': False,  # optional, default is False
            # 'dont_send_headers': False,  # optional, default is False
            # 'magic_response': True,  # optional, default is True
        }
        request.meta['retries'] = 0
        return self.make_dfd(request, spider, item)

    def make_dfd(self, request, spider, item):
        dfd = spider.crawler.engine.download(request, spider)
        dfd.addCallback(self.return_item, item)
        dfd.addErrback(self.process_error, spider, request, item)
        return dfd

    def process_error(self, exception, spider, request, item):
        spider.logger.error(
            '<{}> failed, exception <{}>, message <{}>'.format(spider.name,
                                                               exception.__class__.__name__,
                                                               exception))
        if request.meta['retries'] < self.max_retry:
            request.meta['retries'] += 1
            spider.logger.info(
                '<{}> retrying screenshot request, times = {}'.format(spider.name, request.meta['retries']))
            return self.make_dfd(request, spider, item)
        else:
            spider.logger.warning(
                '<{}> give up screenshot request, times = {}'.format(spider.name, request.meta['retries']))

    def return_item(self, response, item):
        if response.status not in range(200, 300):
            # Error happened, return item.
            return item
        # Save screenshot to file, filename will be hash of url.
        url_hash = sha1(item['url'].encode("utf8")).hexdigest()
        filename = "{}.png".format(url_hash)
        data = response.body
        with open(os.path.join(self.screenshot_dir, filename), "wb") as f:
            f.write(data)
        # Store filename in item.
        item["screenshot_filename"] = filename
        return item
