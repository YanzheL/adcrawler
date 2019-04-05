import os
from hashlib import sha1

import scrapy


class ScreenshotPipeline(object):
    """Pipeline that uses Splash to render screenshot of
    every Scrapy item."""

    def __init__(self, screenshot_dir):
        self.screenshot_dir = screenshot_dir
        os.makedirs(self.screenshot_dir, exist_ok=True)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            crawler.settings['SCREENSHOT_DIR']
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
        dfd = spider.crawler.engine.download(request, spider)
        dfd.addBoth(self.return_item, item)
        return dfd

    def return_item(self, response, item):
        if response.status != 200:
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
