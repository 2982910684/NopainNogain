import scrapy
from toTheMoon.items import TothemoonItem
import time
import sys
import os
import re
import hashlib
from scrapy_redis.spiders import RedisSpider
import logging


class DankoSpider(scrapy.Spider):
    name = 'Danko'
    #allowed_domains = ['www.xxx.com']
    #start_urls = ['http://www.xxx.com/']
    url = 'https://www.amazon.com/s?k=80cc&i=automotive&page=%d'

    start_url = 'https://www.amazon.com/s?k=80cc&i=automotive&page=1'
    page_num = 2



    def __init__(self):
        #讯代理 动态转发
        self.orderno = "ZF202011254931xzj1HT"
        self.secret = "6af156080bfd48b98091db6ff19dd524"
        self.ip_port = "forward.xdaili.cn:80"
        self.timestamp = str(int(time.time()))
        self.string = ("orderno=" + self.orderno + "," + "secret=" + self.secret + "," + "timestamp=" + self.timestamp).encode()
        self.sign = hashlib.md5(self.string).hexdigest().upper()
        self.auth = "sign=" + self.sign + "&" + "orderno=" + self.orderno + "&" + "timestamp=" + self.timestamp
        # 计算耗时
        self.start_time = time.perf_counter()
    #
    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse)

    def parse(self, response):
        page_text = response.text

        pattern_listing = re.compile('<a class="a-link-normal a-text-normal" href="(.*?)">')
        lists = re.findall(pattern_listing,page_text)
        print("获取的url的数量" + str(len(lists)))

        for list in lists:

            url = list.replace('amp;', '')

            item = TothemoonItem()
            new_url = "https://www.amazon.com/" + url
            item['url'] = new_url
            yield scrapy.Request(new_url, callback=self.parse_url, meta={'item': item})

        # 分页
        if (self.page_num <= 5):
            new_url = format(self.url % self.page_num)
            self.page_num += 1
            yield scrapy.Request(url=new_url, callback=self.parse)



    def parse_url(self, response):

        item = response.meta['item']

        page_text = response.text

        #解析ASIN
        pattern_asin = re.compile('data-asin="([A-Z0-9]+)"',re.S)#re.S 表示 .可以匹配任何字符 包括换行符 如果不加不会匹配换行符
        item_asin = re.search(pattern_asin,page_text)
        item['asin'] = item_asin.group(1)

        #通过正则表达式解析数据
        pattern_big = re.compile('#([0-9,]+\sin[A-Za-z &]+)\(')
        item_big = re.findall(pattern_big, page_text)
        if item_big!=None:
            item["rank_big"] = " ".join(item_big)


        pattern_small = re.compile("#(.*?\sin ).*?'>([A-Za-z &]+)</a>")
        items_small = re.findall(pattern_small, page_text)

        list = []
        if items_small != None:
            for item_small in items_small:
                list.append(item_small[0] + item_small[1])
            item["rank_small"] = ";".join(list)


        yield item


        # 统计耗时
        stop_time = time.perf_counter()

        cost = stop_time - self.start_time

        print("%s cost %s second" % (os.path.basename(sys.argv[0]), cost))
