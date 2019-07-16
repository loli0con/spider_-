# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ExamplePipeline(object):
    def process_item(self, item, spider):
        return item


import re


class JokePipeline(object):
    def process_item(self, item, spider):
        item['author'] = re.findall(r'<h2>\n*(.+)\n*</h2>', item['author'])[0]
        item['content'] = (re.findall(r'<span>\s*(.+)\s*</span>', item['content'],
                                      flags=re.DOTALL))[0].replace('<br>', '').replace('\n', '')
        return item


import MySQLdb


class MySQLPipeline(object):
    def open_spider(self, spider):
        db = spider.settings.get('MYSQL_DB_NAME', 'scrapy_default')
        host = spider.settings.get('MYSQL_HOST', 'localhost')
        port = spider.settings.get('MYSQL_PORT', 3306)
        user = spider.settings.get('MYSQL_USER', 'root')
        passwd = spider.settings.get('MYSQL_PASSWORD', 'root')

        self.db_conn = MySQLdb.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset='utf8')
        self.db_cur = self.db_conn.cursor()

    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_conn.close()

    def process_item(self, item, spider):
        self.insert_db(item)
        return item

    def insert_db(self, item):
        values = (
            item['author'],
            item['content'],
        )
        sql = 'INSERT INTO jokes_xujiaxing VALUES (%s,%s)'
        self.db_cur.execute(sql, values)


from pymongo import MongoClient
from scrapy import Item


class MongoDBPineline:
    def open_spider(self, spider):
        db_uri = spider.settings.get('MONGODB_URI', 'mongodb://localhost:27017')
        db_name = spider.settings.get('MONGODB_DB_NAME', 'scrapy_default')

        self.db_client = MongoClient(db_uri)
        self.db = self.db_client[db_name]

    def close_spider(self, spider):
        self.db_client.close()

    def process_item(self, item, spider):
        self.insert_db(item)
        return item

    def insert_db(self, item):
        if isinstance(item, Item):
            item = dict(item)

        self.db.jokes_xujiaxing.insert_one(item)
