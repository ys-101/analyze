# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# 管道1: 终端打印输出
class TencentPipeline(object):
    def process_item(self, item, spider):
        print(dict(item))
        return item

# 管道2:存入MySQL数据库
import pymysql

class TencentMysqlPipeline(object):
    def open_spider(self, spider):
        """爬虫项目启动时,只执行1次,一般用于数据库的连接"""
        print('南山巅上火麟烈')
        self.db = pymysql.connect('localhost','root','123456','tencentdb',charset='utf8')
        self.cur = self.db.cursor()
        self.ins = 'insert into tencenttab values(%s,%s,%s,%s,%s,%s,%s)'

    def process_item(self, item, spider):
        li = [
            item['job_id'],
            item[''
                 'job_name'],
            item['job_type'],
            item['job_city'],
            item['job_time'],
            item['job_require'],
            item['job_duty'],
        ]
        self.cur.execute(self.ins,li)
        self.db.commit()

        return item

    def close_spider(self, spider):
        """爬虫项目结束时,只执行1次,一般用于数据库的断开"""
        print('北海潜深雪饮寒')
        self.cur.close()
        self.db.close()

# 管道3:存入MongoDB数据库
import pymongo
from .settings import *

class TencentMongoPipeline(object):
    def open_spider(self, spider):
        self.conn = pymongo.MongoClient(
            MONGO_HOST, MONGO_PORT
        )
        self.db = self.conn[MONGO_DB]
        self.myset = self.db[MONGO_SET]

    def process_item(self, item, spider):
        self.myset.insert_one(dict(item))

        return item











