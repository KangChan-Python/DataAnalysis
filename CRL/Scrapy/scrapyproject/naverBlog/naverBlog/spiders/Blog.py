# -*- coding: utf-8 -*-
import scrapy


class BlogSpider(scrapy.Spider):
    name = 'Blog'
    allowed_domains = ['www.search.naver.com/search.naver?date_from={시작 날짜}&date_option=8&date_to={마지막 날짜 }&post_blogurl=&post_blogurl_without=&query={검색어}&sm=tab_pge&srchby=all&st=date&where=post&start=1']
    start_urls = ['http://www.search.naver.com/search.naver?date_from={시작 날짜}&date_option=8&date_to={마지막 날짜 }&post_blogurl=&post_blogurl_without=&query={검색어}&sm=tab_pge&srchby=all&st=date&where=post&start=1/']

    def parse(self, response):
        pass
