
import scrapy
from selenium import webdriver
from scrapy import Selector
from scrapy_splash import SplashRequest
from lxml import etree
from lwscrapy.items import TianMaoDataItem, TianMaoDataItemLoader

import re

class TianMaoSpider(scrapy.Spider):

    name = 'tianmaospider'
    allowed_domains = ['taobao.com','detail.tmall.com']
    start_urls = ['https://s.taobao.com/search?q=鞋子&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&style=list']
    items_count = 0
    splash_args = {"lua_source": """
                                --splash.response_body_enabled = true
                                splash.private_mode_enabled = false
                                splash:set_user_agent("Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36")
                                assert(splash:go("https://item.jd.com/5089239.html"))
                                splash:wait(3)
                                return {html = splash:html()}
                                """}

    splah_args = {
        "lua_source": """
            function main(splash, args)
              assert(splash:go(args.url))
              assert(splash:wait(0.5))
              return {
                html = splash:html(),
                png = splash:png(),
                har = splash:har(),
              }
            end
            """
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/72.0.3626.109 Safari/537.36',
    }

    def start_requests(self):

        url = "https://uland.taobao.com/sem/tbsearch?refpid=mm_26632258_3504122_32538762&clk1=04511dd93dde330d86022e9ce3a3dc46&keyword=%E6%89%8B%E6%9C%BA&page=0"

        yield SplashRequest(url, self.parse, endpoint="execute", args=self.splah_args, headers=self.headers)


    # 获取首页列表数据
    def parse(self, respose):
        pattern = re.compile(r'<div class="item">.*?/b></span><span class="listup-tgr-arrow"></span></li></ul></div></div></div></a></div>', re.S)
        res = re.findall(pattern, respose.text)
        # print(res)
        for item in res:

            title = ''
            price = ''
            sales = ''
            shopname = ''
            deatilurl = ''

            try:
                pattern_title = re.compile(r'<span class="title" title=".*?>(.*?)<')
                titles = re.search(pattern_title, item)
                # print('******' * 20 + '\n' + 'title:')
                # print(titles.group(1))
                title = titles.group(1)
            except Exception as e:
                print('error'+str(e))
                title = ''
            try:
                pattern_price = re.compile(r'<span class="pricedetail">¥<strong>(.*?)<')
                prices = re.search(pattern_price, item)
                # print('price:')
                # print(prices.group(1))
                price = prices.group(1)
            except Exception as e:
                print('error' + str(e))
                price = 0

            try:
                pattern_shopname = re.compile(r'<span class="shopNick">(.*?)<')
                shopnames = re.search(pattern_shopname, item)
                # print('shopname:')
                # print(shopnames.group(1))
                shopname = shopnames.group(1)
            except Exception as e:
                print('error' + str(e))
                shopname = ''

            try:
                pattern_sales = re.compile(r'<span class="payNum">(.*?)人付款<')
                saless = re.search(pattern_sales, item)
                # print('sales:')
                # print(saless.group(1))
                sales = saless.group(1)
            except Exception as e:
                # print('error' + str(e))
                sales = 0

            try:
                pattern_url = re.compile(r'<a target="_blank" href="?(.*?)">')
                deatilurls = re.search(pattern_url, item)
                # print('deatilurl:')
                # print(deatilurls.group(1))
                deatilurl = deatilurls.group(1)
            except Exception as e:
                print('error'+str(e))
                deatilurl = ''

            try:
                item = TianMaoDataItem()
                loader = TianMaoDataItemLoader(item=TianMaoDataItem())
                loader.add_value('title', title)
                loader.add_value('price', price)
                loader.add_value('sales', sales)
                loader.add_value('shopname', shopname)
                loader.add_value('deatilurl', deatilurl)

                item = loader.load_item()
                print(item)

                yield scrapy.Request(url=item['deatilurl'], callback=self.deatil_prase, meta={'item': loader})
                # yield item

                # script =
                # """
                #     function main(splash, args)
                #       splash:set_user_agent("Mozilla/5.0  Chrome/69.0.3497.100 Safari/537.36")
                #       splash:go(args.url)
                #       splash:wait(5)
                #       return {html=splash:html()}
                #     end
                # """
                yield SplashRequest(url=item['deatilurl'], callback=self.deatil_prase, endpoint="execute", args=self.splah_args, headers=self.headers)

            except Exception as e:
                print('error'+str(e))

    def deatil_prase(self, respose):
        print('\n' + '******' * 20 + 'deatil_prase' + '*' * 20)
        # print('item:')
        # print(response.meta['item'])
        print('response.body:')
        print(respose.text)

        print('\n' + '******' * 20 + 'deatil_prase' + '*' * 20)