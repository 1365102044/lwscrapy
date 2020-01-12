# -*- coding: utf-8 -*-
import scrapy


class RenrenSpider(scrapy.Spider):
    name = 'renren'
    allowed_domains = ['renren.com', 'httpbin.org/user-agent']
    start_urls = ['http://renren.com/']


    # # 重写 自定义开始请求
    # def start_requests(self):
    #     url = 'http://www.renren.com/PLogin.do'
    #     data = {'email': '1365102044@qq.com',
    #             'password': '1111aaaa'}
    #     request = scrapy.FormRequest(url=url, formdata=data, callback=self.login_prase)
    #     yield request
    #
    # def login_prase(self, response):
    #     print(response.text)
    #     with open('login_res.html', 'w', encoding='utf-8') as ft:
    #         ft.write(response.text)


    # 测试 动态请求头
    def start_requests(self):
        url = 'httpbin.org/user-agent'
        request = scrapy.Request(url=url, callback=self.res_prase)


    def res_prase(self,response):
        print(response.text)
