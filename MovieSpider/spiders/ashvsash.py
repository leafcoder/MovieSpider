# -*- coding: utf-8 -*-
import scrapy
import sqlite3

from scrapy.spiders.crawl import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor

from MovieSpider.settings import SQLITE_FILE, SQLITE_TABLE
from MovieSpider.items import MoviespiderItem

class AshvsashSpider(CrawlSpider):
    name = 'ashvsash'
    allowed_domains = ['m.ashvsash.com']
    start_urls = ['http://m.ashvsash.com/category/电影/']

    rules = [
        Rule(LinkExtractor(allow='page/\d+'), follow=True),
        Rule(LinkExtractor(
            allow='/\d{4}/\d{2}/\d+'), callback='parse_item',
            follow=True, process_links='process_links')
    ]

    def __init__(self):
        CrawlSpider.__init__(self)
        self.sqlite_file  = SQLITE_FILE
        self.sqlite_table = SQLITE_TABLE
        self.conn = sqlite3.connect(self.sqlite_file)

    def parse_item(self, response):
        item = MoviespiderItem()
        article = response.css('div.article_container')
        name  = article.css('h1::text').extract_first()
        image = article.css('.context img::attr(src)').extract_first()
        link  = response.url
        ctime = article.css('.article_info .info_date::text').extract_first()
        category = article.css('.article_info .info_category a::text').extract_first()
        description = article.css('div[id=post_content]').extract_first()
        pan = response.css('.context h2').extract()[-1]
        item['name'] = name
        item['image'] = image
        item['link'] = link
        item['ctime'] = ctime
        item['category'] = category
        item['description'] = description
        item['pan'] = pan
        yield item

    def process_links(self, links):
        for link in links:
            url = link.url
            if url.endswith('/#respond'):
                length = len('/#respond')
                url = url[:-length]
            if url.endswith('/'):
                url = url.strip('/')
            cur = self.conn.execute(
                'select count(*) from tb_link where link=?;',
                (url, ))
            size = cur.fetchone()[0]
            if size == 0:
                yield link