# -*- coding: utf-8 -*-
import scrapy
import time
import json
import pymysql
import re #正则库

from digbit.items_sparkpool import SparkpoolItem
from digbit.database import database

class SparkpoolSpider(scrapy.Spider):
    name = 'sparkpool'
    start_urls = [] #爬行地址
    bar_id = {} #网吧名称 list
    port_list = []

    def __init__(self): #查询获取爬行地址
        self = database.conn(self) #数据库实例
        self.cursor.execute("select url,bar_id from url_list where url like '%sparkpool%'")
        info = self.cursor.fetchall()
        for vo in info:
            before = re.search('.*(?=/#)', vo[0]).group()
            after = re.search('(?<=0x).*', vo[0]).group()
            self.start_urls.append(before+'/api/page/miner?value='+after)
            self.bar_id[vo[0]]=vo[1]

    def parse(self, response): #爬到数据后的回调
        sel = database.conn(self)
        jsons = json.loads(response.body)
        content_all = {} #内容dict
        dict_index = 0  #内容dict 索引
        # print('alive')
        # print(jsons['workers']['data'][0])
        # print('die')
        # print(jsons['workers']['data'][1])
        item = SparkpoolItem()
        for worker in jsons['workers']['data']:
            if worker['hashrate'] <= 0:
                 content = {}
                 content["computer_name"] = worker['rig']
                #  content["computer_name_num"] = re.search('[1-9]\d*', content["computer_name"]).group()
                 content['bar_id'] = self.bar_id[response.url]

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