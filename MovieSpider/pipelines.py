# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3

class MoviespiderPipeline(object):

    def __init__(self, sqlite_file, sqlite_table):
        self.sqlite_file = sqlite_file
        self.sqlite_table = sqlite_table

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            sqlite_file = crawler.settings.get('SQLITE_FILE'),
            sqlite_table = crawler.settings.get('SQLITE_TABLE', 'items')
        )

    def open_spider(self, spider):
        self.conn = sqlite3.connect(self.sqlite_file)

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        keys = item.fields.keys()
        link = item['link']
        cur = self.conn.execute(
            'select count(*) from tb_link where link=?;', (link, ))
        size = cur.fetchone()[0]
        if size == 0:
            insert_sql = "insert into {0}({1}) values ({2})".format(
                self.sqlite_table, 
                ', '.join(keys),
                ', '.join(['?'] * len(keys)))
            values = []
            for key in keys:
                values.append(item.get(key))
            try:
                cur = self.conn.execute(insert_sql, values)
                movie_id = cur.lastrowid
                cur.execute(
                    "insert into tb_link(link, movie_id) values (?, ?);",
                    (link, movie_id))
                self.conn.commit()
            except:
                self.conn.rollback()
                raise
        return item