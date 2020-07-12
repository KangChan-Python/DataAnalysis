# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EcommerceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    maincate = scrapy.Field()
    subcate = scrapy.Field()
    ranking = scrapy.Field()
    title = scrapy.Field()
    oprice = scrapy.Field()
    sprice = scrapy.Field()
    discount = scrapy.Field()
    Fed = scrapy.Field()
