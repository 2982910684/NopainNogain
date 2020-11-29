# NopainNogain
无论我们去到哪里

使用说明：
需要下载的包：
requests
scrapy
scrapy-redis
wheel
pandas
numpy==1.18.4  最新版的有问题，不推荐使用
xlrd
pymongo
lxml
twisted
pywin32
selenium 如果你自己要用的话，本项目不需要


使用前需要手动修改的部分: 
1. Danko.py中的redis ip地址
2. settings.py中的redis地址已经mongodb地址

一、使用讯代理，除了按照说明文档的操作之外，还需要注释一些代码
将scrapy源代码，相对路径为：Lib/site-packages/scrapy/core/downloader/handlers/http11.py的文件中
if isinstance(agent, self._TunnelingAgent):
   headers.removeHeader(b'Proxy-Authorization')
   
二、cookie池
可以在网吧获取（不同机器和不同浏览器）,删除掉多余字段

三、解析网页采用正则表达式
1. 使用findall时只会找出正则表达式中()里的内容，返回列表
2. search会从网页开头开始寻找，直到找到第一个符合的正则表达式返回
3. match会从网页的开头开始匹配，如果不匹配直接返回空，尽量使用search和findall
4. 在正式爬虫之前可以先用demo测试一下爬出的结果，有的时候爬出的页面源码&后面会跟上amp;,'/'变成'%2F',要注意替换掉

四、redis和mongodb的配置文件修改
1. redis：bind 127.0.0.1->0.0.0.0  ,  protect-mode Yes->no
2. mongodb: bind 0.0.0.0

五、使用conda配置环境变量，会更方便

六、使用自己配置的cookie，必须在settings.py中设置 COOKIES_ENABLED = False 

   
   
