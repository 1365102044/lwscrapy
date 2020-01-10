
import scrapy
from lwscrapy.items import GuaziItem

class guaziSpider(scrapy.Spider):

    name = 'guazispider'
    allowed_domains = ['guazi.com']
    start_urls = ['https://www.guazi.com/bj/?ca_kw&ca_n=default&ca_s=seo_baidu']

    def parse(self, response):
        print(response.body)

        # for each in response.xpath('//div[@class="index-carlist-box w1200 js-rec active"]/ul'):
        #     name = each.xpath('li/a/div[@class="car-info"]/h2/text()').extrace_first()
        #     time_s = each.xpath('li/a/div[@class="car-info"]/div/text()')[0].extrace()
        #     distance = each.xpath('li/a/div[@class="car-info"]/div/text()')[2].extrace()
        #     print(name)
        #     print(time_s)
        #     print(distance)
