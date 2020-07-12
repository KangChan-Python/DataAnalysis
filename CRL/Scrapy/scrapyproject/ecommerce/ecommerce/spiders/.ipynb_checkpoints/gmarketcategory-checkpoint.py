# -*- coding: utf-8 -*-
import scrapy


class GmarketcategorySpider(scrapy.Spider):
    name = 'gmarketcategory'
    #allowed_domains = ['corners.gmarket.co.kr/Bestsellers']

    def start_requests(self):
        #무조건 이 함수 먼저 실행
        yield scrapy.Request(url = 'http://corners.gmarket.co.kr/Bestsellers', callback = self.parse)
        #parse 함수에 url 전달
        # yield를 여러개 만들어 각 Request 마다 별도의 함수를 작동시킬 수 있다.
    def parse(self, response):
        category_links = response.css('ul.by-group li a::attr(href)').getall()
        category_names = response.css('ul.by-group li a::text').getall()
        for index, category_link in enumerate(category_links):
            yield scrapy.Request(url='http://corners.gmarket.co.kr/Bestsellers',callback= self.parse_maincategory ,meta ={'maincategory_name':category_names[index]})
    
    def parse_maincategory(self,response):
        print('parse_maincategory ',response.meta['maincategory_name'])
            