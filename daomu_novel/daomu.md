## 关于该爬虫
爬虫功能：利用scrapy 抓取[盗墓笔记](http://www.daomubiji.com/)网站,中各章节的信息，包括书籍名称，章节名称，章节数，章节链接
，章节正文

步骤
1. 前往聚合页  http://www.daomubiji.com/ 获得各个章节的链接（利用Rule,正则）
2. 进入各个章节 的聚合页 如 http://www.daomubiji.com/dao-mu-bi-ji-1
在该章节聚合页上能获得大部分的信息 如 书名，章节名字，章节数，以及章节的链接，先保存至item
3. 通过yield Request(url=url, callback=self.parse_content, meta={"item": item})
继续请求获得的具体章节的链接，以便获得章节正文，并保存至传递的item
4. yield item,在pipelines.py中操作，插入pymongo


## 盗墓爬虫笔记
记录一下自己的学习思路吧

###关于scrapy中的Spider,和CrawlSpider
Spider是最基本的爬虫类

    name 是唯一标识
    allowed_domains 允许爬取的网页范围
    start_urls URL列表，当没有制定特定的URL时，spider将从该列表中开始进行爬取。
    parse 当response没有指定回调函数时，该方法是Scrapy处理下载的response的默认方法。
    
CrawSpider继承了Spider

    多了一个属性：rules 
    包含一个(或多个) Rule对象的集合(list)。 每个 Rule 对爬取网站的动作定义了特定表现。
关于Rule对象

    class scrapy.spiders.Rule(link_extractor, callback=None, cb_kwargs=None, follow=None, process_links=None, process_request=None)    
    
    link_extractor 是一个 Link Extractor 对象。 其定义了如何从爬取到的页面提取链接。
    callback 是一个callable或string(该spider中同名的函数将会被调用)。 从link_extractor中每获取到链接时将会调用该函数。该回调函数接受一个response作为其第一个参数， 并返回一个包含 Item 以及(或) Request 对象(或者这两者的子类)的列表(list)。
    follow 是一个布尔(boolean)值，指定了根据该规则从response提取的链接是否需要跟进。
        也就是说，通过这个规则获取到的链接请求之后的页面，还是否继续用这个规则跟进
        (如果 callback 为None， follow 默认设置为 True ，否则默认为 False) 
    
### 关于Debugger
通过创建Run/Debug Configurations

填写相应参数，详情看下面

[How to use PyCharm to debug Scrapy projects](https://stackoverflow.com/questions/21788939/how-to-use-pycharm-to-debug-scrapy-projects)

### 关于Mongodb 在Linux下的可视化软件
找了很久，没有找到合适好用的，window下的MongoVue好像还不错，在Linux下的，知乎上面推荐了一个Pycharm的插件，我觉得也很棒

[大家在mongodb上使用的GUI工具主要有那些？](https://www.zhihu.com/question/31903748)