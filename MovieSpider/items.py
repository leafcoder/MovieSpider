# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MoviespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name        = scrapy.Field()
    image       = scrapy.Field()
    description = scrapy.Field()
    link        = scrapy.Field()
    ctime       = scrapy.Field()
    category    = scrapy.Field()
    pan         = scrapy.Field()