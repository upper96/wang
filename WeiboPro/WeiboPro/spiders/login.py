# -*- coding: utf-8 -*-
import scrapy
from WeiboPro import slidecode

class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['weibo.cn']
    start_urls = ['https://passport.weibo.cn/signin/login?entry=mweibo&r=https%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt=']

    def parse(self, response):
        pass
