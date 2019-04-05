# Importing base64 library because we'll need it ONLY in case if the proxy we are going to use requires authentication
import logging

from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.exceptions import NotConfigured


# Start your middleware class
class ProxyMiddleware(HttpProxyMiddleware):
    # overwrite process request
    provider = None

    DEFAULT_POOL_KEY = 'ip_list'

    def __init__(self, auth_encoding, pool_conf=None, pool_key=DEFAULT_POOL_KEY):
        super().__init__(auth_encoding)
        self.use_pool = False
        if pool_conf is not None:
            self.use_pool = True
            from redis import Redis
            self.pool = Redis(**pool_conf)
            self.pool_key = pool_key
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('HTTPPROXY_ENABLED'):
            raise NotConfigured
        auth_encoding = crawler.settings.get('HTTPPROXY_AUTH_ENCODING')
        pool_conf = None
        pool_key = cls.DEFAULT_POOL_KEY
        if crawler.settings.getbool('HTTPPROXY_USE_POOL'):
            pool_conf = {
                'host': crawler.settings['HTTPPROXY_POOL_HOST'],
                'port': crawler.settings['HTTPPROXY_POOL_PORT'],
                'password': crawler.settings.get('HTTPPROXY_POOL_PASSWORD', None)
            }
            pool_key = crawler.settings.get('HTTPPROXY_POOL_KEY', cls.DEFAULT_POOL_KEY)
        return cls(
            auth_encoding,
            pool_conf,
            pool_key
        )

    def process_request(self, request, spider):
        if not self.use_pool:
            return super().process_request(request, spider)
        else:
            fetched = self.pool.rpop(self.pool_key)
            if fetched:
                proxy_ip = "http://%s" % fetched
                request.meta['proxy'] = proxy_ip
                self.logger.info('Current used proxy: %s' % proxy_ip)
