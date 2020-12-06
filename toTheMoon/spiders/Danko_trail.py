import scrapy
from toTheMoon.items import AmazonRecordItem
import time
import sys
import os
import re
import hashlib
import pandas as pd

class DankoTrailSpider(scrapy.Spider):
    name = 'Danko_trail'
    # allowed_domains = ['www.xx.com']
    # start_urls = ['http://www.xx.com/']

    def __init__(self):
        # 讯代理 动态转发
        self.orderno = "ZF202011254931xzj1HT"
        self.secret = "6af156080bfd48b98091db6ff19dd524"
        self.ip_port = "forward.xdaili.cn:80"
        self.timestamp = str(int(time.time()))
        self.string = (
                    "orderno=" + self.orderno + "," + "secret=" + self.secret + "," + "timestamp=" + self.timestamp).encode()
        self.sign = hashlib.md5(self.string).hexdigest().upper()
        self.auth = "sign=" + self.sign + "&" + "orderno=" + self.orderno + "&" + "timestamp=" + self.timestamp
        # 计算耗时
        self.start_time = time.perf_counter()
        # pandas列表
        amazon_df = pd.read_excel('E:/amazon-2020.12.1.xlsx') #需自己配置

        self.url_list = amazon_df['url'].tolist()

    def start_requests(self):
        for url in self.url_list:
            item = AmazonRecordItem()
            item['url'] = url
            yield scrapy.Request(url=url, callback=self.parse, meta={'item': item})

    def parse(self, response):
        item = response.meta['item']
        print(item['url'])
        page_text = response.text

        # 解析ASIN
        pattern_asin = re.compile('data-asin="([A-Z0-9]+)"', re.S)  # re.S 表示 .可以匹配任何字符 包括换行符 如果不加不会匹配换行符
        item_asin = re.search(pattern_asin, page_text)
        if item_asin!=None:
            item['asin'] = item_asin.group(1)

        # 通过正则表达式解析数据
        # 解析大类排名
        pattern_big = re.compile('#([0-9,]+\sin[A-Za-z &]+)\(')
        item_big = re.findall(pattern_big, page_text)
        if item_big != None:
            item["rank_big"] = " ".join(item_big)
            print(" ".join(item_big))

        # 解析小类排名
        pattern_small = re.compile("#(.*?\sin ).*?'>([A-Za-z &]+)</a>")
        items_small = re.findall(pattern_small, page_text)
        list = []
        if items_small != None:
            for item_small in items_small:
                list.append(item_small[0] + item_small[1])
            item["rank_small"] = ";".join(list)
            print(";".join(list))

        yield item

        # 统计耗时
        stop_time = time.perf_counter()

        cost = stop_time - self.start_time

        print("%s cost %s second" % (os.path.basename(sys.argv[0]), cost))
