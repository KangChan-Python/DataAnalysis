# -*- coding: utf-8 -*-
import scrapy
from ecommerce.items import EcommerceItem


class GmarketcategorySpider(scrapy.Spider):
    name = 'gmarketcategory'
    #allowed_domains = ['corners.gmarket.co.kr/Bestsellers']
    
    def start_requests(self):
        #무조건 이 함수 먼저 실행
        yield scrapy.Request(url='http://corners.gmarket.co.kr/Bestsellers',
                                callback=self.parse_maincategory)
        #parse 함수에 url 전달
        # yield를 여러개 만들어 각 Request 마다 별도의 함수를 작동시킬 수 있다.
    def parse_maincategory(self, response):
        category_links = response.css('ul.by-group li a::attr(href)').getall()
        category_names = response.css('ul.by-group li a::text').getall()
        #1st category
        for index, category_link in enumerate(category_links):
            yield scrapy.Request(url='http://corners.gmarket.co.kr'+ category_link,
            callback= self.parse_item ,meta ={'maincategory_name':category_names[index],'subcategory_name':'ALL'})
        #2nd category
        for index, category_link in enumerate(category_links):
            yield scrapy.Request(url='http://corners.gmarket.co.kr'+ category_link,
            callback= self.parse_subcategory ,meta ={'maincategory_name':category_names[index]})
        
    def parse_subcategory(self,response):
        subcategory_links = response.css('div.navi.group ul li a::attr(href)').getall()
        print(len(subcategory_links))
        subcategory_names = response.css('div.navi.group ul li a::text').getall()
        for index2, subcategory_link in enumerate(subcategory_links):
            
            yield scrapy.Request(url = 'http://corners.gmarket.co.kr'+ subcategory_link,
            callback= self.parse_item, meta ={'maincategory_name':response.meta['maincategory_name'],'subcategory_name':subcategory_names[index2]})

    def parse_item(self,response):
        print('parse_category : ', response.meta['maincategory_name'], response.meta['subcategory_name'])
        
        best_items = response.css('div.best-list')
        for index, item in enumerate(best_items[1].css('li')):
            doc = EcommerceItem()  
            # .css 메소드 다시 사용 가능
            name = item.css('a.itemname::text').get()
            
            oprice = item.css('div.o-price span::text').get()
            sprice = item.css('div.s-price strong span span::text').get()
            discount = item.css('div.s-price em::text').get()
            Fedex = item.css('div.icon img::attr(alt)').get() 
            if oprice == None:
                oprice = sprice

            if discount == None:
                discount = '0'
            else:
                discount = discount.replace('%','')

            if Fedex == None:
                Fedex = '유료배송'
            oprice = int(oprice.replace('원','').replace(',',''))
            sprice = int(sprice.replace('원','').replace(',',''))
            doc['maincate'] = response.meta['maincategory_name']
            doc['subcate'] = response.meta['subcategory_name']
            doc['title'] =name
            doc['ranking'] = index +1
            doc['oprice']= oprice
            doc['sprice'] = sprice
            doc['discount'] = discount
            doc['Fed'] = Fedex
            yield doc