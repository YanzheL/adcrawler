# encoding=utf-8
import sys

from scrapy import cmdline

if __name__ == '__main__':
    cmd = 'scrapy crawl {}'.format(sys.argv[1])
    cmdline.execute(cmd.split())
    # cmdline.execute('scrapy crawl dataSpider'.split())
