# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from soHu.dataloader import SohuLoader
from soHu.items import SohuuniversalItem

class SohuSpider(CrawlSpider):
    name = 'sohu'
    allowed_domains = ['www.sohu.com']
    start_urls = ['http://www.sohu.com/c/8/1461']
    allow = r'www.sohu.com/a/\d+_\d+'
    restrict_xpath = r'//div[@data-role="news-item"]'
    rules = (
        Rule(LinkExtractor(allow=allow,restrict_xpaths = restrict_xpath),callback='parse_item'),
    )

    def parse_item(self, response):
        # item = {}
        loader = SohuLoader(item=SohuuniversalItem(), response=response)
        loader.add_xpath('title','//div[@class="text-title"]/h1/text()') #新闻标题
        loader.add_value('url',response.url)
        loader.add_xpath('datetime','//div[@class="text-title"]/div/span[@class="time"]/text()')
        loader.add_xpath('text', '//article/p/text()')
        yield loader.load_item()
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
