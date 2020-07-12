# -*- coding: utf-8 -*-
import scrapy
from ecommerce.items import EcommerceItem

class GmarketSpider(scrapy.Spider):
    name = 'gmarket'
    #allowed_domains = ['www.gmarket.co.kr'] # 이것을 포함한 도메인만 크롤링 하겠다 -> Option
    start_urls = ['http://corners.gmarket.co.kr/Bestsellers/'] #안에 url 두개 가능

    def parse(self, response):
        titles = response.css('div.best-list li a::text').getall()
        prices = response.css('div.s-price strong span::text').getall()
        for title, price in zip(titles,prices):
            item = EcommerceItem()
            item['price'] = int(price.strip().replace('원','').replace(',', ''))
            item['title'] = title
            yield item # 반복마다 items.py title 필드에 데이터가 쌓인다.