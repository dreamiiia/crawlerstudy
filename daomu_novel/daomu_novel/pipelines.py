# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo
from scrapy.conf import settings


class DaomuNovelPipeline(object):
    # 初始化设置
    def __init__(self):
        host = settings["MONGODB_HOST"]
        port = settings["MONGODB_PORT"]
        dbname = settings["MONGODB_DBNAME"]  # 数据库名字
        docname = settings["MONGODB_DOCNAME"] # 数据集合（文件）名字
        client = pymongo.MongoClient(host=host, port=port)  # 建立于MongoClient 的连接
        db = client[dbname]  # client.douban / client['douban']  得到数据库
        self.collection = db[docname]  # db.book / db['book']   得到数据集合

    def process_item(self, item, spider):
        bookinfor = dict(item)
        self.collection.insert(bookinfor)
        return item
