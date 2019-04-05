import pymongo
from twisted.internet.threads import deferToThread


class MongoPipeline(object):

    def __init__(self, host, port, db, user, password, collection, repl=None):
        self.mongo_uri = "mongodb://%s:%s@%s:%s" % (user, password, host, port)
        self.mongo_opt = {} if repl is None else {
            'replicaset': repl,
            'readPreference': 'secondaryPreferred'
        }
        self.db_name = db
        self.collection_name = collection

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings['MONGO_HOST'],
            port=crawler.settings['MONGO_PORT'],
            db=crawler.settings['MONGO_DB'],
            user=crawler.settings['MONGO_USER'],
            password=crawler.settings['MONGO_PASSWORD'],
            collection=crawler.settings['MONGO_COLLECTION'],
            repl=crawler.settings['MONGO_REPL']
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host=self.mongo_uri, **self.mongo_opt)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        return deferToThread(self._insert, item, spider)

    def _insert(self, item, spider):
        self.collection.insert_one(dict(item))
        spider.logger.info('Inserted {} to MongoDB'.format(dict(item)))
        return item
