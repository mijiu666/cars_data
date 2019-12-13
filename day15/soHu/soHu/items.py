# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose


def getNewTime(value):
    newTime=value.split('·')[0].strip()
    return newTime
def getNewTitle(value):
    title = value.strip()
    return title

class SohuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class SohuuniversalItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field(input_processor=MapCompose(getNewTitle))
    datetime = scrapy.Field(input_processor=MapCompose(getNewTime))
    text = scrapy.Field()
    url = scrapy.Field()