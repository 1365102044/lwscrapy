# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags

class LwscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    pass

class GuaziItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    time_s = scrapy.Field()
    distance = scrapy.Field()





# 移除特定字符
def remove_ivaliedchar(str):
    return str.replace('\u200b', '')

# 不做整体出来（既是不再取列表中的第一个非空值了）
def return_value(value):
    return value

# 字符拼接
def add_baseurl(value):
    return 'http://yao.xywy.com'+value

def to_list(value):
    list = []
    list.append(value)
    return list

# 从图片url中切出特殊标识当做图片名字
def get_image_name(value):
    return value.split('/')[-2]

# 定义一个默认输出的
class ArticalItemLoader(ItemLoader):
    # 实现之前的extract_first()方法
    # 这里只是重载这个属性，设置为只选取第一个值
    default_output_processor = TakeFirst()


class MedicaldataItem(scrapy.Item):
    # 药名
    name = scrapy.Field()
    # 生成企业
    company = scrapy.Field()
    # 功能
    function = scrapy.Field(
        input_processor = MapCompose(remove_tags, remove_ivaliedchar)
    )
    # 详情URL
    deatil_url = scrapy.Field(
        input_processor = MapCompose(add_baseurl)
    )
    # 审批编号
    approval_num = scrapy.Field()
    # 相关疾病
    related_disease = scrapy.Field()
    # 图片url
    image_url = scrapy.Field(
        # 维持该字段是数组形式（图片下载管道中间件需要）
        input_processor = MapCompose(to_list,),
        # 数据输出格式，使用不做特殊处理（屏蔽掉：取第一个非空数据/TakeFirst()）
        output_processor = MapCompose(return_value)
    )
    # 图片名
    image_name = scrapy.Field(
        input_processor = MapCompose(get_image_name)
    )




# 天猫 数据
class TianMaoDataItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

class TianMaoDataItem(scrapy.Item):
    title = scrapy.Field()
    sales = scrapy.Field()
    price = scrapy.Field()
    deatilurl = scrapy.Field()
    shopname = scrapy.Field()


class JingDongDataItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
class JingDongDataItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    sku_id = scrapy.Field()
    deatilurl = scrapy.Field()
    commentsnum = scrapy.Field()



class JdCommentsItem(scrapy.Item):
    sku_id = scrapy.Field()
    content = scrapy.Field()
    creationTime = scrapy.Field()
    productColor = scrapy.Field()
    productSize = scrapy.Field()