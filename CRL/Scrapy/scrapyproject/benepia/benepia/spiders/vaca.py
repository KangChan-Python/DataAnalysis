# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
from loginform import fill_login_form
class VacaSpider(scrapy.Spider):
    name = 'vaca'
    # login_user = 'vacation_ftest01'
    # login_password = '1566@skmns'
    def start_requests(self):
        
        yield scrapy.Request(url= 'https://korean.visitkorea.or.kr/main/cs_main.do' , callback = self.local_parse)

    def local_parse(self,response):
        numpage = ['{}'.format(i) for i in range(1,9)]
        numpage += ['{}'.format(i) for i in range(31,40)]
        numpage.append('All')    
        for num in numpage:
            yield scrapy.Request(url = 'https://korean.visitkorea.or.kr/list/cs_list.do?areacode=' + num , meta= {'num': num}, callback = self.course_parse )

    def course_parse(self,response):
        for i in range(1,10):
            try:
                #print(i)
                return scrapy.FormRequest.from_response(response, formdata = {'cmd': 'COURSE_CONTENT_LIST_VIEW', 'month' : 'All', 'areaCode': response.meta['num'], 'sigunguCode' : 'All', 'tagId' : 'All', 'sortkind' : 3 , 'page' : '{}'.format(i) ,'cnt' : 10 } , callback = self.get_item  )
            except:
                pass
    def get_item(self,response):
            print(1)
            first = response.css('li:nth-child(1) div.area_txt div a::text').get()
            print(first)    