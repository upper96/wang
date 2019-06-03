# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import redis
#
# class WeiboproPipeline(object):
#
#     def open_spider(self,spider):
#         self.rds = redis.StrictRedis(host='123.56.23.174',password='wang1997',port=6379,db=3)
#
#
#     def process_item(self, item, spider):
#         print(item)
#         self.rds.lpush("weibo",str(item))
#
#         return item


from twisted.enterprise import adbapi
import hashlib
from WeiboPro.settings import mysql_host,mysql_port,mysql_db,mysql_passwd,mysql_user

class WeiboproPipeline(object):
    def open_spider(self,spider):
        self.dbpool = adbapi.ConnectionPool('pymysql',host= mysql_host, port=mysql_port,user=mysql_user, passwd=mysql_passwd, db=mysql_db, charset="utf8",use_unicode=True)
    def close_spider(self,spider):
        self.dbpool.close()
    def process_item(self,item,spider):
        self.dbpool.runInteraction(self.insert,item)

    def insert(self,tx,item):
        T=item['categary']

        if 'YC'in T:
            insert_sq1_detail_sql = 'insert into weibo(text,qg) values( "%s","%s")'
            tx.execute(insert_sq1_detail_sql, (item["content"],item["qingganzhi"]))
        else:
            insert_sq1_detail_sql = 'insert into weibo(text,qg) values( "%s","%s")'
            tx.execute(insert_sq1_detail_sql, (item["liyou"], item["qingganzhi"]))