# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymongo

class MongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db,mongo_port):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.port = mongo_port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
            mongo_port=crawler.settings.get('MONGO_PORT')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host=self.mongo_uri,port=self.port)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        name = item.__class__.__name__
        self.db[name].insert_one(dict(item))
        return item
