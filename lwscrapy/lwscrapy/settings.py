# -*- coding: utf-8 -*-

# Scrapy settings for lwscrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import os

BOT_NAME = 'lwscrapy'

SPIDER_MODULES = ['lwscrapy.spiders']
NEWSPIDER_MODULE = 'lwscrapy.spiders'

FEED_EXPORT_ENCODING = 'utf-8'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 5 # 访问频率控制（s）

# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16     #每个域名最多发送请求数量
#CONCURRENT_REQUESTS_PER_IP = 16        #每个ip并发数量

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False    #请求携带cookie

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False      #监听爬虫当前状态和指标，开始暂停等

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'lwscrapy.middlewares.LwscrapySpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'lwscrapy.middlewares.LwscrapyDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# 管道 值越小优先级越高
# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'lwscrapy.pipelines.LwscrapyPipeline': 300,
   #  自己重写的图片下载管道中间件
   'lwscrapy.pipelines.ImagesnamePipelines': 310,
    # 天猫数据
    'lwscrapy.pipelines.lwTianMaoPipelines': 299,
    # 京东
    'lwscrapy.pipelines.lwJDPipelines': 289,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

#定义爬取深度
# DEPTH_LIMIT = 2
# DEPTH_PRIORITY = 0#广度或者深度优先
#自定义去重方式
#默认方式DUPEFILTER_CLASS = "scrapy.dupefilters.RFPDupeFilter"
# DUPEFILTER_CLASS = "jianshu_spider.duplication.RepeatFilter"


##########DB setting ############
# DB = {  #key务必大写
# 'host': '127.0.0.1',
# 'port': 3306,
# 'user' : 'root',
# 'password' : '1234567890',
# 'database' : 'medicaldata',
# 'charset' : 'utf8'
# }

# 关闭的条件*********
# 关闭定时任务：
# 一个整数值，单位为秒。如果一个spider在指定的秒数后仍在运行， 它将以 closespider_timeout 的原因被自动关闭。 如果值设置为0（或者没有设置），spiders不会因为超时而关闭。
# CLOSESPIDER_TIMEOUT = 0
# 在抓取了指定数目的Item之后关闭
# CLOSESPIDER_ITEMCOUNT = 100
# 在收到了指定数目的响应之后关闭
CLOSESPIDER_PAGECOUNT = 1000
# 在发生了指定数目的错误之后就终止爬虫程序
# CLOSESPIDER_ERRORCOUNT = 0


# log配置
LOG_FILE = 'medicaldataspider.log'
LOG_LEVEL = 'INFO'


# 图片下载 （需要先配置图片下载管道中间件）
#在item中定义图片url的字段，ImagesPipeline会自动下载这个url地址
IMAGES_URLS_FIELD = "image_url"
#存放的路径,根目录下的img文件夹
IMAGES_STORE = os.path.join(os.path.abspath(os.path.dirname(__file__)), "img/medicaldataspider")




# 配置splash

# Splash服务器地址
SPLASH_URL = 'http://localhost:8050'
DOWNLOADER_MIDDLEWARES = {
'scrapy_splash.SplashCookiesMiddleware': 723,
'scrapy_splash.SplashMiddleware': 725,
'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

SPIDER_MIDDLEWARES = {
'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}
# 设置去重过滤器
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
# 用来支持cache_args
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'


# 爬取的数据类型
JDspider_KEYWORDS = ['手机']