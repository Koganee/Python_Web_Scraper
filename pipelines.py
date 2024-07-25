# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo

from scrapy import settings
from scrapy.exceptions import DropItem
import logging

class StackPipeline:
    def process_item(self, item, spider):
        return item


class MongoDBPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        return cls(
            mongodb_server=crawler.settings.get('MONGODB_SERVER', 'localhost'),
            mongodb_port=crawler.settings.get('MONGODB_PORT', 27017),
            mongodb_db=crawler.settings.get('MONGODB_DB', 'scrapy_db'),
            mongodb_collection=crawler.settings.get('MONGODB_COLLECTION', 'scrapy_collection')
        )

    def __init__(self, mongodb_server, mongodb_port, mongodb_db, mongodb_collection):
        self.mongodb_server = mongodb_server
        self.mongodb_port = mongodb_port
        self.mongodb_db = mongodb_db
        self.mongodb_collection = mongodb_collection

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongodb_server, self.mongodb_port)
        self.db = self.client[self.mongodb_db]
        self.collection = self.db[self.mongodb_collection]

    def close_spider(self, spider):
        self.client.close()


    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                spider.logger.debug("False!")
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert_one(ItemAdapter(item).asdict())
            spider.logger.debug("Question added to MongoDB database!")
        return item
