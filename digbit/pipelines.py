# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import datetime
import time
import json
from digbit.database import database

class DigbitPipeline(object):
    # 清库
    # def __init__(self):
    #     self = database.conn(self) #数据库实例
    #     self.cursor.execute('truncate table close_list')
    #     self.db.commit()
    def process_item(self, item, spider):
        self = database.conn(self) #数据库实例
        if spider.name == 'f2pool' or spider.name == 'sparkpool' or spider.name == 'uupool':

            content = item['scan_content']

            content_data = json.loads(content)
            comp_name_list = [] #第三方网站所有网吧list
            port_list = [] #缓存本次关闭端口列表，重复端口只写一次
            now_bar_id = 0 #当前查询的网吧
            now_bar_comp_list = [] #当前网吧所有端口+电脑名称 list
            all_bar_comp_name = [] #当前网吧所有电脑名称list
            no_find_list = [] #库里有但第三方网站没有的网吧名称
            
            for info in content_data:
                computer_name = content_data[info]['computer_name']
                bar_id = content_data[info]['bar_id']
                port_id = content_data[info]['port_id']
                comp_name_list.append(computer_name)

                #根据bar_id 获取网吧对应所有电脑列表
                if now_bar_id != bar_id:
                    now_bar_comp_list = []
                    now_bar_id = bar_id
                    self.cursor.execute("select bp.id,bp.comp_id from board_list as b INNER join board_port_list as bp on b.id = bp.board_id where bp.close_time>0 and b.bar_id = "+str(bar_id)+" and bp.comp_id <> ''")
                    bar_comp_list = self.cursor.fetchall()
                    for comp_list in bar_comp_list:
                        foo = []
                        foo.append(comp_list[0])
                        foo.append(comp_list[1])
                        for voo in comp_list[1].split(','):
                            all_bar_comp_name.append(voo)
                        now_bar_comp_list.append(foo)

                #重复端口id只写一次
                if port_id not in port_list:
                    #端口id不为0写入
                    if port_id != 0:
                        port_list.append(port_id)
                        sql =  "INSERT INTO close_list(bar_id, computer_name ,board_port_id,created_at) VALUES  ('"+str(bar_id)+"','"+computer_name+"','"+str(port_id)+"',NOW())"
                        self.cursor.execute(sql)
            print('comp_name_list',comp_name_list)
            #遍历 将所有未出现的电脑名称写入 no_find_list
            #for comp in all_bar_comp_name:
            #    if comp not in comp_name_list:
            #        no_find_list.append(comp)

            # 未找到列表寻找端口
            #for comp in no_find_list:
            #    for vo in now_bar_comp_list:
            #        #找到端口，写入库
            #        if comp in vo[1].split(','):
            #            #重复端口id只写一次
            #            if vo[0] not in port_list:
            #                 #端口id不为0写入
            #                if port_id != 0:
            #                    port_list.append(vo[0])
            #                    sql =  "INSERT INTO close_list(bar_id, computer_name ,board_port_id,created_at) VALUES  ('"+str(bar_id)+"','"+comp+"','"+str(vo[0])+"',NOW())"
            #                    self.cursor.execute(sql)

            try:
                self.db.commit()
            except Exception as e:
                print(e)
                self.db.rollback()
        elif spider.name == 'vvpool':
            pass
        return item
                