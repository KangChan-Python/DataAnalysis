# -*- coding: utf-8 -*-
import scrapy


class PopupSpider(scrapy.Spider):
    name = 'Popup'
    allowed_domains = ['www.korean.visitkorea.or.kr/main/main.do']
    start_urls = ['https://www.korean.visitkorea.or.kr/main/main.do/']

    def parse(self, response):
        
