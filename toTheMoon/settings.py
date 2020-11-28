# Scrapy settings for toTheMoon project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'toTheMoon'

SPIDER_MODULES = ['toTheMoon.spiders']
NEWSPIDER_MODULE = 'toTheMoon.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

LOG_LEVEL = 'ERROR'


# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#开启headers设置cookie的配置
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
  'Accept-Language':'h-CN,zh;q=0.9',
  'accept-encoding':'gzip, deflate',
  'upgrade-insecure-requests':'1',
}
#download_timeout = 10



# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'AmazonTest.middlewares.AmazontestSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
#See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'toTheMoon.middlewares.TothemoonDownloaderMiddleware': 543,

}


# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   #'AmazonTest.pipelines.mysqlPipeline': 300,
   'toTheMoon.pipelines.MongoPipeline': 300,
    #存取结果放入到redis
   #'scrapy_redis.pipelines.RedisPipeline': 301,
}
MONGO_URI='localhost'
MONGO_DATABASE='Amazon'
MONGO_PORT=27017



#MONGD_URI ='mongodb://admin:root@192.168.110.177:27017'

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


#REDIS_URL = 'redis://192.168.:6379'
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

#scrapy-redis
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# # 是否允许暂停
# SCHEDULER_PERSIST = True
# # 去调度器中获取数据时，如果为空，最多等待时间（最后没数据，未获取到）。
# SCHEDULER_IDLE_BEFORE_CLOSE = 10
#
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'