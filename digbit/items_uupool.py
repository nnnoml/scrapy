# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UupoolItem(scrapy.Item):

    scan_url = scrapy.Field()
    scan_content  = scrapy.Field()