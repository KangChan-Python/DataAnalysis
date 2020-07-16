# -*- coding: utf-8 -*-
import scrapy


class BlogSpider(scrapy.Spider):
    name = 'Blog'
    #allowed_domains = ['www.search.naver.com/search.naver?date_from={시작 날짜}&date_option=8&date_to={마지막 날짜 }&post_blogurl=&post_blogurl_without=&query={검색어}&sm=tab_pge&srchby=all&st=date&where=post&start=1']
    
    def start_requests(self):
        yield scrapy.Request(url = 'http://www.search.naver.com/search.naver?date_from={20200712}&date_option=8&date_to={20200712}&post_blogurl=&post_blogurl_without=&query={통영+맛집}&sm=tab_pge&srchby=all&st=date&where=post&start={}/'.format(i), callback=parse_mainFrame)
    
    def parse_mainFrame
        

    def parse(self, response):
        pass
