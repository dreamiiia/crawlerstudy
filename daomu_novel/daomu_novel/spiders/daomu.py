# -*-coding:utf-8-*-

from scrapy.spiders import CrawlSpider, Spider, Rule  # 使用CrawlSpier这个进化类，同时导入Rule对象，用来定义爬取动作
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor  # 定义了如何从爬取到的页面提取链接
from daomu_novel.items import DaomuNovelItem  # 导入容器


# 先用Spider类，熟悉一下
# 创建我自己的爬虫类，继承CrawlSpider
class DaomuSpider(CrawlSpider):
    name = "daomu"  # 唯一标识
    # allowed_domains = ["http://www.daomubiji.com"]  # 一个范围
    allowed_domains = ["daomubiji.com"]  # 域名范围
    start_urls = ["http://www.daomubiji.com"]  # URL列表
    # rules 是 Rule对象的集合; LinkExtractor 的 allow 用正则表达式提取符合的链接
    # 这里的callback string(该spider中同名的函数将会被调用)
    rules = (
        Rule(LinkExtractor(allow=(r"http://www.daomubiji.com/\S+",)), callback="parse_item"),
    )

    def parse_item(self, response):  # 默认使用parse方法来处理
        article = response.xpath("//article")
        for i in article:
            item = DaomuNovelItem()  # 实例化自己定义的item
            book_infor = i.xpath("a/text()").extract()[0].split(" ")
            item["bookname"] = book_infor[0] if len(book_infor) < 4 else ",".join(book_infor[:2])
            item["chapnum"] = book_infor[1] if len(book_infor) < 4 else book_infor[2]
            try:
                item["chapname"] = book_infor[2] if len(book_infor) < 4 else book_infor[3]
            except Exception as e:
                print(e)
                item["chapname"] = '无'
            url = i.xpath("a/@href").extract()[0]
            item["chapurl"] = url
            yield Request(url=url, callback=self.parse_content, meta={"item": item})  # 注意callback

    def parse_content(self, response):
        chaptext = response.xpath("//article/p/text()").extract()
        item = response.meta["item"]
        item["chaptext"] = "/".join(chaptext).replace("\u3000", "")
        yield item


