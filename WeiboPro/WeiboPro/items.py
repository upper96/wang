# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboproItem(scrapy.Item):
    # 分析：微博共有四种，即原创不带图、原创带图、转发不带图、转发带图
    # 公共部分
    # 微博类型
    categary = scrapy.Field()
    # 博主名字
    name = scrapy.Field()
    # 文字内容
    content = scrapy.Field()
    # 点赞数
    dianzan = scrapy.Field()
    # 评论数
    pinglun = scrapy.Field()
    # 转发数
    zhuanfa = scrapy.Field()

    # 其他部分
    # 图片
    pic = scrapy.Field()
    # 转发理由
    liyou = scrapy.Field()

    #情感值
    qingganzhi = scrapy.Field()


    pass
