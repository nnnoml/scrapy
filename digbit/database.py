# -*- coding: utf-8 -*-

# 数据库实例

import pymysql


class database():
    def conn(self):
        self.db = pymysql.connect(
            host='127.0.0.1',
            user='root',
            passwd='root',
            db='guanji',
            charset='utf8'
            )
        self.cursor = self.db.cursor()
        return self