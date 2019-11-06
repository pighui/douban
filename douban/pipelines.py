# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv

import pymysql
from pymysql.cursors import DictCursor
from douban import settings


class DoubanPipeline(object):
    def __init__(self):
        # **dict 将字典转成关键参数传值的格式，如key = value
        self.conn = pymysql.Connect(**settings.DB_CONFIG)
        self.init_db()

    def init_db(self):
        with self.conn.cursor(cursor=DictCursor) as c:
            c.execute('drop table if exists douban_movie')
            sql = '''
            create table douban_movie(id integer PRIMARY key auto_increment,
                                m_name varchar(20),
                                m_director varchar(200),
                                m_score float,
                                m_comment varchar(50),
                                m_detail varchar(50))
            '''
            c.execute(sql)

    def process_item(self, item, spider):
        with self.conn.cursor(cursor=DictCursor) as c:
            sql = "insert into douban_movie(%s) values(%s)"
            cols = ", ".join('`{}`'.format('m_' + k) for k in item.keys())
            val_cols = ', '.join('%({})s'.format(k) for k in item.keys())
            res_sql = sql % (cols, val_cols)
            c.execute(res_sql, args=item)
            self.conn.commit()
        return item

    def close_spider(self, spider):
        self.conn.cursor().close()
        self.conn.close()


class MoviePipeline(object):
    def __init__(self):
        self.csv_filename = 'top250.csv'
        self.existed_header = False

    def process_item(self, item, spider):
        with open(self.csv_filename, 'a', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=item.keys())
            if not self.existed_header:
                writer.writeheader()
                self.existed_header = True
            writer.writerow(item)
        return item