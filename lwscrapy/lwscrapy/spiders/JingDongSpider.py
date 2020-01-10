
from scrapy import Spider
from scrapy_splash import SplashRequest
import re
from lwscrapy.items import JingDongDataItemLoader, JingDongDataItem, JdCommentsItem

class JDSpider(Spider):

    name = 'jdspider'
    allowed_domains = ['jd.com']
    start_urls = [
        'https://search.jd.com/Search?keyword=手机&enc=utf-8&wq=shou%27ji&pvid=e7fb5f90acee4b9c9bab98c19545d571']
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

        url = "https://search.jd.com/Search?keyword=手机&enc=utf-8&wq=shou%27ji&pvid=e7fb5f90acee4b9c9bab98c19545d571"

        yield SplashRequest(url, self.parse, endpoint="execute", args=self.splah_args, headers=self.headers)


    def parse(self, response):
        # print('\n'+'*'*20)
        # print(response.text)
        # print('\n' + '*' * 20)
        # print(type(response.text))
        pat = re.compile(r'<li class="gl-item" data-sku=[\s\S]*?<i class="goods-icons4 J-picon-tips" data-tips=".*?">')
        items = re.findall(pat, response.text)
        # print(len(items))
        for item in items:
            sku_id = re.search(r'.*?data-sku="(\d+)".*?', item).group(1)
            title_deatilurl = re.search(r'.*?target="_blank" title="(.*?)" href="(.*?)" onclick=', item)
            title = title_deatilurl.group(1)
            deatilurl = title_deatilurl.group(2)
            price = re.search(r'.*?<em>￥</em><i>(.*?)</i></strong>.*?', item).group(1)
            commentsnum = re.search(r'[\s\S]*?flagsClk=.*?">(.*?)</a>条评价</strong>', item).group(1)

            # print(sku_id)
            # print(deatilurl)
            # print(title)
            # print(price)
            # print(commentsnum)
            num = 0
            if '万' in commentsnum:
                num = int(commentsnum.split('万')[0])*10000
            # print(num)
            loader = JingDongDataItemLoader(item=JingDongDataItem())
            loader.add_value('title', title)
            loader.add_value('sku_id', sku_id)
            loader.add_value('deatilurl', deatilurl)
            loader.add_value('price', price)
            loader.add_value('commentsnum', num)
            item = loader.load_item()
            # print(item)
            yield item
            page = 0

            headers = {'Referer': 'https://item.jd.com/{}.html'.format(sku_id),
                       'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
            while page < 10:

                url_deatil = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv22316&productId={}&score=0&sortType=5&page={}&pageSize=10&isShadowSku=0&fold=1'.format(sku_id,page)

                print(url_deatil)

                yield SplashRequest(url=url_deatil, headers=headers, args=self.splash_args, callback=self.deatilPrase, meta={'skuid': sku_id})

                page = page + 1


    def deatilPrase(self, respose):
        print('\n' + '*' * 20)
        # print(respose.text)
        print('\n' + '*' * 20)
        skuid = respose.meta['skuid']
        print(skuid)
        items = re.findall(r'{"id":\d+,"guid":".*?afterDays":\d+}', respose.text)
        print(len(items))
        for item in items:

            # res = re.findall(r'.*?"content":"([\s\S]*?).*?"creationTime":"([\s\S]*?)[\s\S]*?productColor="(.*?).*?"productSize":"(.*?)",.*?')
            content = re.search(r'"content":"([\s\S]*?)","', item).group(1)
            creationTime = re.search(r'"creationTime":"([\s\S]*?)","isDelete"', item).group(1)
            productColor = re.search(r'"productColor":"(.*?)","productSize"', item).group(1)
            productSize = re.search(r'"productSize":"(.*?)",', item).group(1)


            # print(content)
            # print(creationTime)
            # print(productColor)
            # print(productSize)
            item = JdCommentsItem()
            item['sku_id'] = skuid
            item['content'] = content
            item['creationTime'] = creationTime
            item['productColor'] = productColor
            item['productSize'] = productSize

            print(item)
            yield item
