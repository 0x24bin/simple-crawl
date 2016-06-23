# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
from pymongo import MongoClient
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
########################################################################
class MongoDBPipeline:
    """"""
    #----------------------------------------------------------------------
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            item['hasScaned']=0
            self.collection.insert(dict(item))
            log.msg("Question added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
#            self.collection.insert({'hasScaned':0})
        return item

class FiveurlPipeline(object):
    def process_item(self, item, spider):
        return item
