# -*- coding: utf-8 -*-
import scrapy
import json
from time import sleep
from WeiboPro.items import WeiboproItem
from urllib import parse as url_parse
import snownlp

class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['weibo.cn']
    # start_urls = ['https://weibo.cn/']

    # 重写start_requests方法，进行下载的截取
    def start_requests(self):
        url = 'https://weibo.cn/search/mblog?hideSearchFrame=&keyword={}&page={}'
        keyword = input("关键字：")
        cur_page = input('输入页码：')
        ky = url_parse.quote(keyword)
        # 在这里给下载器加入cookie
        cookies = json.load(open("E:/WeiboPro/cookie.json"))["cookie"]
        print(cookies)
        for page in range(1,int(cur_page)):
            if page==30 or page == 40 or page == 60 or page == 80:
                sleep(10)
            cur_url = url.format(ky, page)
            print(cur_url)
            yield scrapy.Request(url=cur_url,cookies=cookies,callback=self.parse)


    def parse(self, response):
        # print(response.text)
        # 【解析】
        weibo_list = response.xpath("//div[@class='c' and @id]")
        # 对所有的页面上的微博做一个划分
        for weibo in weibo_list:
            # 找到微博里面的div
            div_list = weibo.xpath("./div")
            item = WeiboproItem()
            if len(div_list) == 1:
                # 原创不带图
                item["categary"] = "YC NO PIC"
                item["name"] = weibo.xpath(".//a[@class='nk']/text()").extract_first()
                item["content"] = "\n".join(weibo.xpath(".//span[@class='ctt']//text()").extract())
                item["dianzan"] = weibo.xpath(".//div/a/text()").extract()[-4]
                item["pinglun"] = weibo.xpath(".//div/a/text()").extract()[-2]
                item["zhuanfa"] = weibo.xpath(".//div/a/text()").extract()[-3]
                q = snownlp.SnowNLP("\n".join(weibo.xpath(".//span[@class='ctt']//text()").extract()))
                qingganzhi = q.sentiments
                item["qingganzhi"]=float(qingganzhi)

            elif len(div_list) == 2:

                item["name"] = weibo.xpath(".//a[@class='nk']/text()").extract_first()
                item["content"] = "\n".join(weibo.xpath(".//span[@class='ctt']//text()").extract())
                item["dianzan"] = weibo.xpath(".//div[2]/a/text()").extract()[-4]
                item["pinglun"] = weibo.xpath(".//div[2]/a/text()").extract()[-2]
                item["zhuanfa"] = weibo.xpath(".//div[2]/a/text()").extract()[-3]
                # 通过退图片进一步区分
                img_src = weibo.xpath(".//img[@class='ib']/@src")
                if len(img_src) > 0:
                    # 原创带图
                    item["categary"] = "YC PIC"
                    item["pic"] = img_src.extract_first()
                    q = snownlp.SnowNLP("\n".join(weibo.xpath(".//span[@class='ctt']//text()").extract()))
                    qingganzhi = q.sentiments
                    item["qingganzhi"] = float(qingganzhi)
                else:
                    # 转发不带图
                    item["categary"] = "ZF NO PIC"
                    item["liyou"] = weibo.xpath(".//div[2]//text()").extract()[1]
                    q = snownlp.SnowNLP(weibo.xpath(".//div[2]//text()").extract()[1])
                    qingganzhi = q.sentiments
                    item["qingganzhi"] = float(qingganzhi)
            else:
                # 转发带图
                item["categary"] = "ZF PIC"
                item["name"] = weibo.xpath(".//a[@class='nk']/text()").extract_first()
                item["content"] = "\n".join(weibo.xpath(".//span[@class='ctt']//text()").extract())
                item["dianzan"] = weibo.xpath(".//div[3]/a/text()").extract()[-4]
                item["pinglun"] = weibo.xpath(".//div[3]/a/text()").extract()[-2]
                item["zhuanfa"] = weibo.xpath(".//div[3]/a/text()").extract()[-3]

                item["pic"] = weibo.xpath(".//img[@class='ib']/@src").extract_first()
                item["liyou"] = weibo.xpath(".//div[3]//text()").extract()[1]
                q = snownlp.SnowNLP(weibo.xpath(".//div[3]//text()").extract()[1])
                qingganzhi = q.sentiments
                item["qingganzhi"] = float(qingganzhi)

            print(item)
            yield item


        # # 【翻页】
        # # 解析出下一页id值
        # next_url ="https://weibo.cn" + response.xpath("//div[@class='pa']//a[1]/@href").extract_first()
        # print(next_url)
        # sleep(1)
        # yield scrapy.Request(url=next_url,callback=self.parse)









