# -*- coding: utf-8 -*-
import scrapy
from naverBlog.items import NaverblogItem
#from bs4 import BeautifulSoup

class BlogSpider(scrapy.Spider):
    name = 'Blog'
    #allowed_domains = ['www.search.naver.com/search.naver?date_from={시작 날짜}&date_option=8&date_to={마지막 날짜 }&post_blogurl=&post_blogurl_without=&query={검색어}&sm=tab_pge&srchby=all&st=date&where=post&start=1']


    def start_requests(self):
        # numstr = input('시작 날짜와 마지막 날짜를 입력해주세요 : ')
        # fromdate , todate = numstr.split()[0], numstr.split()[1]
        # search = input('포함할 검색어를 입력해주세요 : ')
        # search_without =input('제외할 검색어를 입력해주세요 : ')
        # with1 =''
        
        # for index ,i in enumerate(search.strip().split()):
        #     with1 += i
        #     if not index == len(search.strip().split())-1:
        #         with1 += '+'
        # without = with1
        # for index, i in enumerate(search_without.strip().split()):
        #     without += '-' +i
        # print(fromdate, todate, with1, without)
        # print(f'https://search.naver.com/search.naver?date_from={fromdate}&date_option=8&date_to={todate}&dup_remove=1&nso=p%3Afrom{fromdate}to{todate}&post_blogurl=&post_blogurl_without={without}&query={with1}&sm=tab_pge&srchby=all&st=sim&where=post&start=1')
        #  yield scrapy.Request(url = f'https://search.naver.com/search.naver?date_from={fromdate}&date_option=8&date_to={todate}&dup_remove=1&nso=p%3Afrom{fromdate}to{todate}&post_blogurl=&post_blogurl_without={without}&query={with1}&sm=tab_pge&srchby=all&st=sim&where=post&start=1', callback=self.parse_first)
        yield scrapy.Request(url = 'https://search.naver.com/search.naver?where=post&query=%ED%86%B5%EC%98%81%20%EB%A7%9B%EC%A7%91%20-%EC%9E%A5%EB%A1%80%EC%8B%9D%EC%9E%A5%20-%EA%B2%BD%EC%A3%BC%20-%EB%B6%80%EC%82%B0%20-%EC%B0%BD%EC%9B%90%EC%B9%98%ED%82%A8%20-%EC%A3%BC%EB%AC%B8%EB%AC%B8%EC%9D%98%20-%EA%B0%95%EC%9B%90%EB%8F%84&st=sim&sm=tab_opt&date_from=20200712&date_to=20200712&date_option=8&srchby=all&dup_remove=1&post_blogurl=&post_blogurl_without=&nso=so%3Ar%2Ca%3Aall%2Cp%3Afrom20200712to20200712&where=post&start=1', callback = self.parse_first)

    def parse_first(self,response):
        # pagen = response.xpath('//*[@id="elThumbnailResultArea"]').get()
        # print(pagen)
        pagen = response.css('#main_pack > div.blog.section._blogBase._prs_blg > div > span::text').get()
        
        pagen = int(pagen.split('/')[1].replace('건',''))
        pagen = pagen // 10
        pageurl = str(response)[5 :len(str(response)) -2]   

        pagenum =pagen*10 +1    
        
        for index in range(1, pagenum, 10):
            yield scrapy.Request(url= pageurl + str(index), callback = self.parse_blogurl)

    def parse_blogurl(self, response):
        urls =[]
        for index in range(1,11):
            sindex = str(index)
            url = response.css(f'#sp_blog_{sindex} > dl > dt > a::attr(href)').get()
            page_url = response.url
            yield scrapy.Request(url=url ,callback =self.parse_mainFrame, meta = {'pageurl' : page_url,'index':sindex} )
        
            

    def parse_mainFrame(self,response):
        mainFrame = response.css('#mainFrame::attr(src)').get()
        try:
            trueFrame = mainFrame[:len(str(mainFrame))- 5] +'True'
        except TypeError:
            print(mainFrame)
        print("https://blog.naver.com" + trueFrame)
        
        yield scrapy.Request(url = "https://blog.naver.com" + trueFrame,callback = self.parse_item, meta = {'pageurl': response.meta['pageurl'],'index':response.meta['index']})

    def parse_item(self,response):
        
        doc = NaverblogItem()
        doc['link'] = response.url
        span = response.css('div.pcol1 > div.se_editArea > div > div > div > h3::text').get()
        if span == None:
            span = response.css('div.pcol1 h3::text').get()
        if span == None:
            span = response.css('div.htitle span::text').get()
        if span.strip() == '':
            span = response.css('div.se_textView h3::text').get()
        
        if span == None or span.strip() =='':
            print(i)
        #SEDOC-1594480384069-397240049 > div:nth-child(3) > div > div > div.pcol1 > div.se_editArea > div > div > div > h3
        # try:
        #     text = response.css('div.se-main-container span::text').getall()
        #     doc['context'] = text
        #se-module.se-module-text.se-title-text
        # except:
        #     print(1)
        doc['title']  =span
        text = response.css('div.se-main-container span::text').getall()
        text2 =response.css('div.postViewArea div div::text').getall()
        text3 =response.css('div.post-view222028850841 p span strong').getall()
        if text == []:
            text = response.css('span.se-fs-fs16.se-ff-nanumsquare::text').getall()

        if text ==[]:
            text = response.css('p.se_textarea::text').getall()
        
        if text == []:
            text =response.css('div.postViewArea div p span::text').getall()
        
        if text ==[]:
            text =response.css('div p span::text').getall()
        
        if text == []:
            text = response.css('div.se-module.se-module-text span::text').getall()
      
        if text ==[]:
            text = response.css('div.se-fs-.se-ff-nanumsquare span::text').getall()
        if text ==[]:
            text = response.css('div.se-fs-.se-ff- s span strong::text').getall()
        if text == []:
            text = response.css('div.se-fs-.se-ff-system span::text').getall()
        text = ' '.join(text)
        text2 = ' '.join(text2)
        text3 = ' '.join(text3)
        text += "\n" + text2 +text3
        doc['index'] = response.meta['index']
        doc['context'] =text
        doc['pageurl'] = response.meta['pageurl']
        
        yield doc

 