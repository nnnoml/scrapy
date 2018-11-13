# -*- coding: utf-8 -*-
import scrapy
import time
import json
import pymysql
import re #正则库

from digbit.items_uupool import UupoolItem
from digbit.database import database

class UupoolSpider(scrapy.Spider):
    name = 'uupool'
    start_urls = [] #爬行地址
    bar_id = {} #网吧名称 list

    def __init__(self): #查询获取爬行地址
        self = database.conn(self) #数据库实例
        self.cursor.execute("select url,bar_id from url_list where url like '%uupool%'")
        info = self.cursor.fetchall()
        for vo in info:
            #爬虫地址数组
            self.start_urls.append(vo[0])
            #额外拿出板子id string
            self.cursor.execute("select id from board_list where bar_id = "+str(vo[1]))
            board_info = self.cursor.fetchall()
            board_list = ''
            for vo2 in board_info:
                board_list += str(vo2[0])+','
            board_list = board_list[:-1]
            #根据板子id 获取所有机器名称
            self.cursor.execute("select comp_id from board_port_list where board_id in ("+board_list+")")
            machine_info = self.cursor.fetchall()
            machine_list = ''
            for vo3 in machine_info:
                if vo3[0] != '':
                    machine_list += str(vo3[0])+','
            machine_list = machine_list[:-1]
            machine_list = machine_list.split(',')
            #网吧id和网吧机器映射
            self.bar_id[vo[1]]=machine_list

    def parse(self, response): #爬到数据后的回调
        sel = database.conn(self)
        content_all = {} #内容dict
        dict_index = 0  #内容dict 索引
        for vo in response.xpath('//*[@id="online-list"]/tr'): #xpath截取数据
            item = UupoolItem()
            content = {}
            computer_name = vo.xpath('td[2]')
            
            content["computer_name"] = computer_name.xpath('string(.)').extract()[0]

            # 默认网吧id 0 ，根据电脑名称遍历所有网吧机器，获取对应网吧id
            content["bar_id"] = 0
            for idx in self.bar_id:
                if content["computer_name"].lower() in self.bar_id[idx]:
                    content["bar_id"] = idx
                    break

            # content["computer_name_num"] = re.search('[1-9]\d*', content["computer_name"]).group() #电脑名称取数字
            # content["bar_id"] = self.bar_id[response.url]

            #查询要关闭的端口号
            # print('sql:'+"select bp.id from board_list as b INNER join board_port_list as bp on b.id = bp.board_id where bp.close_time>0 and b.bar_id = "+str(content['bar_id'])+" and FIND_IN_SET('"+str(content['computer_name'])+"',bp.comp_id)")
            sel.cursor.execute("select bp.id from board_list as b INNER join board_port_list as bp on b.id = bp.board_id where bp.close_time>0 and b.bar_id = "+str(content['bar_id'])+" and FIND_IN_SET('"+str(content['computer_name'])+"',bp.comp_id)")
            port_id = sel.cursor.fetchone()
            if port_id is None:
                content['port_id'] = 0
            else:
                content['port_id'] = port_id[0]
      
            content_all[dict_index] = content #附加到dict
            dict_index += 1

        item['scan_url'] = response.url #本次爬取url
        item['scan_content']  = json.dumps(content_all,ensure_ascii=False) #数据格式为json
        yield item

    # def detail(self,response):
        # return str(response.body, encoding='utf-8')
