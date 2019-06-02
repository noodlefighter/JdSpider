# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

class JdjdPipeline(object):

    def __init__(self):
        self.conn = pymysql.connect('localhost','root','root','jdspider', charset='utf8') 
        self.cursor = self.conn.cursor()

    def process_item(self,item,spider):

        # sql语句
        insert_sql = """
        insert into data(id,title,url,price,brand,model,color,ratio,resolution,refresh_rate,luminance) VALUES('%s','%s','%s',%f,'%s','%s','%s','%s','%s','%s','%s')
        """ % (item['id'],item['title'],item['url'],item['price'],item['brand'],item['model'],item['color'],item['ratio'],item['resolution'],item['refresh_rate'],item['luminance'])

        # 执行插入数据到数据库操作
        self.cursor.execute(insert_sql)
        # 提交，不进行提交无法保存到数据库
        self.conn.commit()

        # return item
 
    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()