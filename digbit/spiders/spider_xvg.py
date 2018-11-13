# -*- coding: utf-8 -*-
import scrapy
import time
import json
import pymysql
from digbit.items_xvg import XvgItem
from digbit.database import database

class VvpoolSpider(scrapy.Spider):
    name = 'xvg'
    start_urls = [] #爬行地址
    username = [] #登录帐号
    password = [] #登录密码

    bar_id = [] #网吧id list
    index = 0 #网吧id索引

    def __init__(self): #查询获取爬行地址
        self = database.conn(self) #数据库实例
        self.cursor.execute("select bit_url,bar_id,web_username,web_password from bd_bit_type_config \
                where bit_url like '%xvg%' group by bit_url")
        info = self.cursor.fetchall()
        for vo in info:
            self.start_urls.append(vo[0])
            self.username.append(vo[2])
            self.password.append(vo[3])
            self.bar_id.append(vo[1])

    def parse(self, response): #爬到数据后的回调
        content_all = {} #内容dict
        dict_index = 0  #内容dict 索引
        for sel in response.xpath('//*[@id="b-workers"]/tr'): #xpath截取数据
            item = XvgItem() 
            
            content = {}
            content["computer_name"] = str(sel.xpath('td[1]/text()').extract()[0])
            content["Hashrate"] = str(sel.xpath('td[2]/text()').extract()[0])
            content["Difficulty"] = str(sel.xpath('td[3]/text()').extract()[0])
            content["time_local"] = time.time()
            content_all[dict_index] = content #附加到dict

            dict_index += 1
            # time_local = float(sel.xpath('td[5]/script').re('\d+\.?\d*')[0])
            # item['date'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_local))
            # url = self.base_url + item['computer_name'][0]
            # item['detail'] = scrapy.Request(url,headers=self.headers,callback=self.detail) #深度爬取
        item['scan_url'] = response.url #本次爬取url
        item['scan_content']  = json.dumps(content_all,ensure_ascii=False) #数据格式为json
        self.index += 1
        yield item