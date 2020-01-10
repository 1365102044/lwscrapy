# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from twisted.enterprise import adbapi
from pymysql import cursors
from lwscrapy.items import MedicaldataItem, JdCommentsItem, JingDongDataItem

from scrapy.pipelines.images import ImagesPipeline

from scrapy import Request


class lwBasePipelines(object):
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '1234567890',
            'database': 'lwqdata',
            'charset': 'utf8',
            'cursorclass': cursors.DictCursor
        }
        self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)


class lwJDPipelines(object):
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '1234567890',
            'database': 'lwqdata',
            'charset': 'utf8',
            'cursorclass': cursors.DictCursor
        }
        self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)

    def process_item(self, item, spider):

        if spider.name is not 'jdspider':
            return item

        # 使用twisted将MySQL插入变成异步执行。通过连接池执行具体的sql操作，返回一个对象
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 添加异常处理
        query.addCallback(self.handle_error)
        return item

    def do_insert(self, cursor, item):
        sql = ''
        values = []
        if isinstance(item, JingDongDataItem):
            sql = '''
            insert into jd_t (title, price, sku_id, deatilurl, commentsnum) values (%s, %s, %s, %s, %s)
            '''
            values = (item['title'], item['price'], item['sku_id'], item['deatilurl'], item['commentsnum'])
        elif isinstance(item, JdCommentsItem):
            sql = '''
            insert into jd_comment_t (sku_id, content, creationTime, productColor, productSize) values (%s, %s, %s, %s, %s)
            '''
            values = (item['sku_id'], item['content'], item['creationTime'], item['productColor'], item['productSize'])
        else:
            return item
        # print('*' * 30)
        # print(sql)
        cursor.execute(sql, values)

    def handle_error(self, failure):
        if failure:
            print(failure)



class lwTianMaoPipelines(object):

    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '1234567890',
            'database': 'lwqdata',
            'charset': 'utf8',
            'cursorclass': cursors.DictCursor
        }
        self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)

    def process_item(self, item, spider):

        if spider.name is not 'tianmaospider':
            return item

        # 使用twisted将MySQL插入变成异步执行。通过连接池执行具体的sql操作，返回一个对象
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 添加异常处理
        query.addCallback(self.handle_error)
        return item

    def do_insert(self, cursor, item):

        sql = '''
        insert into tianmao_t (title, sales, price, shopname) values (%s, %s, %s, %s)
        '''
        values = (item['title'], item['sales'], item['price'], item['shopname'])
        # print('*' * 30)
        # print(sql)
        cursor.execute(sql, values)

    def handle_error(self, failure):
        if failure:
            print(failure)


class ImagesnamePipelines(ImagesPipeline):

    # 1看源码可以知道，这个方法只是遍历出我们指定的图片字段，是个数组，然后一个一个请求
    def get_media_requests(self, item, info):
        if isinstance(item, MedicaldataItem):
            # 循环每一张图片地址下载，若传过来的不是集合则无需循环直接yield
            for imageurl in item['image_url']:
                print('imagepipelines.imageurl:')
                print(imageurl)
                # meta里面的数据是从spider获取，然后通过meta传递给下面方法：file_path
                yield Request(imageurl, meta={'name': item['image_name']})
        else:
            return item

    # 2重命名，若不重写这函数，图片名为哈希，就是一串乱七八糟的名字
    def file_path(self, request, response=None, info=None):
        filename = request.meta['name']
        # 注意，需要拼接后缀，不然文件格式不是图片，无法打开
        return filename+'.jpg'


    #3这个是请求完成之后走的方法，我们可以得到请求的url和存放的地址
    def item_completed(self, results, item, info):
        pass



def lwstring(self, str):
    return pymysql.escape_string(str)

class LwscrapyPipeline(object):



    # def __init__(self,):
    #     self.conn = pymysql.connect(host='127.0.0.1',
    #                                 port=3306,
    #                                 user='root',
    #                                 passwd='1234567890',
    #                                 db='medicaldata',
    #                                 charset='utf8',
    #                                 use_unicode = True)
    #     self.cursor = self.conn.cursor()
    #
    # # 必需函数
    # def process_item(self, item, spider):
    #     # print(item)
    #     sql = '''
    #     insert into medicaldata_t (name, company, deatil_url, approval_num, related_disease, func,image_url,image_name) values (%s, %s, %s, %s, %s, %s, %s, %s) ON duplicate key update name = values(name)
    #     '''
    #     function = self.conn.escape_string(item['function'])
    #     # print('function:'+function)
    #     # function = function.replace('\u200b', '')
    #     # print('function:' + function)
    #     values = (item['name'], item['company'], item['deatil_url'], item['approval_num'], item['related_disease'], function, item['image_url'][0], item['image_name'])
    #     # print(sql)
    #     print(values)
    #     self.cursor.execute(sql, values)
    #     self.conn.commit()
    #
    #     #  返回是为了把数据传给下一个管道
    #     return item
    #
    # def close_spider(self, spider):
    #     self.cursor.close()
    #     self.conn.close()



    # 采用异步数据库连接池的方法
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '1234567890',
            'database': 'medicaldata',
            'charset': 'utf8',
            'cursorclass': cursors.DictCursor
        }
        self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        # self._sql = None

    # @property
    # def sql(self):
    #     if not self._sql:
    #         self.sql = '''
    #         insert into medicaldata_t (name, company, deatil_url, approval_num, related_disease, func,image_url,image_name) values (%s, %s, %s, %s, %s, %s, %s, %s) ON duplicate key update name = values(name)
    #         '''
    #         return self._sql
    #     return self._sql

    # @classmethod
    # def form_settings(cls, settings):
    #
    #     adbparams = dict(
    #         host=settings('MYSQL_HOST'),
    #         database=settings("MYSQL_DATABASE"),
    #         user=settings("MYSQL_USER"),
    #         password=settings("MYSQL_PASSWORD"),
    #         port=settings("MYSQL_PORT"),
    #         cursorclass=pymysql.cursors.DictCursor,  #指定cursor类型
    #     )
    #     # 连接数据池ConnectionPool，使用pymysql或者Mysqldb连接
    #     dbpool = adbapi.ConnetionPool('pymysql', **adbparams)
    #
    #     return cls(dbpool)

    # def open_spider(self, spider):
    #     self.db = pymysql.connect(self.host, self.user, self.password,self.database, charset='utf8', port=self.port)
    #     print('*'*10+'open')
    #     print(self.db)
    #     self.cursor = self.db.cursor()
    #
    # def close_spider(self, spider):
    #     print('*'*10+'close')
    #     self.cursor.close()
    #     self.db.close()

    def process_item(self, item, spider):

        if spider.name is not 'lw_medicaldataspider':
            return item

        # 使用twisted将MySQL插入变成异步执行。通过连接池执行具体的sql操作，返回一个对象
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 添加异常处理
        query.addCallback(self.handle_error)
        return item


    def do_insert(self, cursor, item):
        sql = '''
        insert into medicaldata_t (name, company, deatil_url, approval_num, related_disease, func,image_url,image_name) values (%s, %s, %s, %s, %s, %s, %s, %s) ON duplicate key update name = values(name)
        '''
        values = (item['name'], item['company'], item['deatil_url'], item['approval_num'], item['related_disease'], item['function'], item['image_url'][0], item['image_name'])
        print('*' * 30)
        print(sql)
        cursor.execute(sql, values)

    def handle_error(self, failure):
        if failure:
            print(failure)

