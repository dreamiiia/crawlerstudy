# -*- coding: utf-8 -*-

# Scrapy settings for daomu_novel project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'daomu_novel'

SPIDER_MODULES = ['daomu_novel.spiders']
NEWSPIDER_MODULE = 'daomu_novel.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112'

# Obey robots.txt rules
ROBOTSTXT_OBEY = None
COOKIES_ENABLED = True

ITEM_PIPELINES = {
   'daomu_novel.pipelines.DaomuNovelPipeline': 300,
}

MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_DBNAME = 'daomu'
MONGODB_DOCNAME = 'book2'


