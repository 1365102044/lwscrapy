
import scrapy
from lwscrapy.items import MedicaldataItem, ArticalItemLoader


class MedicaldataSpider(scrapy.Spider):

    # 爬虫的唯一识别名称
    name = 'lw_medicaldataspider'

    #爬取起始URL 爬虫从这里开始抓取数据，所以，第一次下载的数据将会从这些urls开始。其他子URL将会从这些元祖URL中继承性生成。
    start_urls = ['http://yao.xywy.com/class/4-0-0-1-0-1.htm']

    # 搜索的域名范围
    # 规定爬虫只爬取这个域名下的网页，不存在的URL会被忽略。
    allowed_domains = ['yao.xywy.com',
                       'http://xs3.op.xywy.com']

    def parse(self, response):

        response.xpath('/html/head/title/text()')
        # items = []
        for each in response.xpath('//div[@class="h-drugs-item"]'):

            item = MedicaldataItem()
            item_loader = ArticalItemLoader(item=MedicaldataItem(), selector=each)

            item_loader.add_xpath('name', 'div/a/@target')
            item_loader.add_xpath('company', 'div/span/text()')
            item_loader.add_xpath('function', 'div[2]/div[2]/div[2]/text()')
            item_loader.add_xpath('deatil_url', 'div[2]/div[1]/a/@href')
            item_loader.add_xpath('image_url', 'div[2]/div[1]/a/img/@src')
            item_loader.add_xpath('image_name', 'div[2]/div[1]/a/img/@src')
            item = item_loader.load_item()


            # item = MedicaldataItem()
            # #extract()方法返回的都是unicode字符串
            # name = each.xpath('div/a/@target').extract_first()
            # company = each.xpath('div/span/text()').extract_first()
            # function = each.xpath('div[2]/div[2]/div[2]/text()').extract_first()
            #
            # item['name'] = name
            # item['company'] = company
            # item['function'] = function

            #
            # deatil_url = 'http://yao.xywy.com'+each.xpath('div[2]/div[1]/a/@href').extract_first()
            # image_url = each.xpath('div[2]/div[1]/a/img/@src').extract_first()
            # item['deatil_url'] = deatil_url
            # imageurl_list = []
            # imageurl_list.append(image_url)
            # item['image_url'] = imageurl_list
            # image_name = image_url.split('/')[-2]
            # item['image_name'] = image_name


            yield scrapy.Request(url=item['deatil_url'], callback=self.deatil_parse, meta={'item': item_loader})
            # 结束本次，继续循环
            # break

        # return items


    # 详情页面的回调
    def deatil_parse(self, response):
        # filename = "deatil.html"
        # open(filename, 'wb').write(response.body)
        itemloader = response.meta['item']
        styles = {}
        # 获取编号
        for each in response.xpath('//div[@class="phonebox fl pz-box"]//span[@class="r-rumbox"]/b'):
            cont = each.xpath('text()').extract_first()
            style = each.xpath('@style').extract_first()

            style_list = list(style)[0:len(style)-3]
            # print(style_list)
            tem = style_list[6:len(style_list)]
            str_tem = ''.join(tem)
            styles.update({int(str_tem): cont})

        number = self.handle_num(styles)
        itemloader.add_value('approval_num', number)
        # item['approval_num'] = number

        # 相关疾病
        related_diseases = []
        for each in response.xpath('//div[@class="d-info-dl mt20"]/dl[4]/dd/a'):
            t = each.xpath('text()').extract_first()
            related_diseases.append(t)
        # item['related_disease'] = ','.join(related_diseases)
        related_disease = ','.join(related_diseases)
        itemloader.add_value('related_disease',related_disease)
        item = itemloader.load_item()
        print('related_disease：'+item['related_disease'])

        yield item

    #处理编号
    def handle_num(self, styles_dic):
        # print(styles_dic)
        sort_list = sorted(styles_dic.keys())
        sort_list.reverse()
        res = []
        for each in sort_list:
            res.append(styles_dic[each])
        return ''.join(res)






