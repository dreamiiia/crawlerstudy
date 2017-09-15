# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DaomuNovelItem(scrapy.Item):
    # define the fields for your item here like:
    bookname = scrapy.Field()  # 书的名字
    chapnum =scrapy.Field()  # 第几个章节
    chapname = scrapy.Field()  # 章节名字
    chapurl = scrapy.Field()  # 章节链接
    chaptext = scrapy.Field()  # 章节正文
