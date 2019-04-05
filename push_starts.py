import json

from scrapy.utils.project import get_project_settings

from adcrawler.scrapy_redis_bf import connection

server = connection.from_settings(get_project_settings())

if __name__ == '__main__':
    urls = [
        'https://finance.sina.com.cn/',
        'http://business.sohu.com'
    ]
    for url in urls:
        task = {
            'url': url,
            'cur_depth': 0
        }
        server.lpush("AdUrlSpider:url_tasks", json.dumps(task))
        print(task)
