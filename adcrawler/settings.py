# -*- coding: utf-8 -*-

# Scrapy settings for adcrawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import os

BOT_NAME = 'adcrawler'

SPIDER_MODULES = ['adcrawler.spiders']
NEWSPIDER_MODULE = 'adcrawler.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'adcrawler (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    'adcrawler.middlewares.spider_middleware.AdcrawlerSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'adcrawler.middlewares.midproxy.ProxyMiddleware': 800,
    'adcrawler.middlewares.rotate_useragent.RotateUserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    # 'adcrawler.middlewares.PipecrawlerDownloaderMiddleware': 543,
    'adcrawler.middlewares.wait_random_sec.WaitRandomSecMiddleware': 543,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'adcrawler.pipelines.UrlPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
LOG_FORMATTER = 'adcrawler.utils.log_formatter.PoliteLogFormatter'
SCHEDULER = "adcrawler.scrapy_redis_bf.scheduler.Scheduler"
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = 'adcrawler.scrapy_redis_bf.queue.SpiderPriorityQueue'
DUPEFILTER_CLASS = "adcrawler.scrapy_redis_bf.dupefilter.RFPDupeFilter"
DUPEFILTER_DEBUG = True
MEDIA_ALLOW_REDIRECTS = True

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = int(os.getenv('CONCURRENT_REQUESTS', 32))

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
RETRY_TIMES = int(os.getenv('RETRY_TIMES', 2))
SCREENSHOT_RETRY_TIMES = int(os.getenv('SCREENSHOT_RETRY_TIMES', 5))

# Config  about redis
REDIS_HOST = os.getenv('REDIS_HOST', '10.245.146.40')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)

FILTER_HOST = os.getenv('FILTER_HOST', '10.245.146.40')
FILTER_PORT = int(os.getenv('FILTER_PORT', 6379))
FILTER_PASSWORD = os.getenv('FILTER_PASSWORD', None)

SPLASH_URL = os.getenv('SPLASH_URL', 'http://10.245.146.40:8050')

MONGO_HOST = os.getenv('MONGO_HOST', '10.245.146.100')
MONGO_PORT = int(os.getenv('MONGO_PORT', 37017))
MONGO_DB = os.getenv('MONGO_DB', 'ad_data')
MONGO_USER = os.getenv('MONGO_USER', 'manager-rw')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD', 'HITdbManager-rw!')
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION', 'data')
MONGO_REPL = os.getenv('MONGO_REPL', 'nistmain')

IMAGES_MIN_HEIGHT = int(os.getenv('IMAGES_MIN_HEIGHT', 0))
IMAGES_MIN_WIDTH = int(os.getenv('IMAGES_MIN_WIDTH', 90))
IMAGES_URLS_FIELD = os.getenv('IMAGES_URLS_FIELD', 'ad_img_urls')
IMAGES_RESULT_FIELD = os.getenv('IMAGES_RESULT_FIELD', 'ad_img_paths')
IMAGES_STORE = os.getenv('IMAGES_STORE', 'images/ad')
SCREENSHOT_DIR = os.getenv('SCREENSHOT_DIR', 'images/screenshots')

RANDOM_WAIT_INTERVAL_RANGE = int(os.getenv('RANDOM_WAIT_INTERVAL_RANGE', 20))

DOWNLOAD_TIMEOUT = int(os.getenv('DOWNLOAD_TIMEOUT', 30))

MAX_URL_TASKS = int(os.getenv('MAX_URL_TASKS', 20000))
RECURSIVE_CHECK_DEPTH = int(os.getenv('RECURSIVE_CHECK_DEPTH', 4))
MAX_TASK_DEPTH = int(os.getenv('MAX_TASK_DEPTH', 100))
