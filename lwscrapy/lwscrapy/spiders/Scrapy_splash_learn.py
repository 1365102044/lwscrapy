
import scrapy
from selenium import webdriver
from scrapy import Selector
from scrapy_splash import SplashRequest


class Scrapy_splash(scrapy.Spider):

    name = 'scrapy_splash'
    allowed_domains = ['taobao.com']
    start_urls = ['http://stock.qq.com/l/stock/ywq/list20150423143546.htm']
    items_count = 0

    def start_requests(self):
        script = """
                        function main(splash, args)
                          splash:set_user_agent("Mozilla/5.0  Chrome/69.0.3497.100 Safari/537.36")
                          splash:go(args.url)
                          splash:wait(5)
                          return {html=splash:html()}
                        end
                    """
        url = "https://uland.taobao.com/sem/tbsearch?refpid=mm_26632258_3504122_32538762&clk1=04511dd93dde330d86022e9ce3a3dc46&keyword=%E6%89%8B%E6%9C%BA&page=0"
        yield SplashRequest(url, self.parse, endpoint="execute", args={'lua_source': script, 'url': url})


    def parse(self, respose):
        # sel = scrapy.Selector(respose)

        # links = sel.xpath("//div[@class='qq_main']//ul[@class='listInfo']//li//div[@class='info']//h3//a/@href").extract()
        # print(links)
        print(respose.text)