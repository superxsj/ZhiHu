# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import  Item ,Field

class userItem(Item):
    # define the fields for your item here like:
    follower_count = Field()
    headline = Field()
    name = Field()
    url_token = Field()

#123456
#change in master and dev
