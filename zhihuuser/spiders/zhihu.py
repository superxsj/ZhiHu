# -*- coding: utf-8 -*-
import json

import requestes as requestes
import scrapy
from scrapy import Request,Spider

from zhihuuser.items import *


class ZhihuSpider(Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    follow_url = 'https://www.zhihu.com/api/v4/members/{name}/followees?include={include}&offset={offset}&limit={limit}'
    start_user = 'tianshansoft'
    follow_qurry = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    user_url = 'https://www.zhihu.com/api/v4/members/{name}?include={include}'
    user_qurry = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'

    def start_requests(self):
        yield  Request(self.user_url.format(name = self.start_user,include = self.user_qurry),callback=self.parse_user)
        yield  Request(self.follow_url.format(name = self.start_user,include = self.follow_qurry,offset = 0,limit = 20),callback=self.parse_follows)

    def parse_follows(self, response):
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(name = result.get('url_token'),include = self.user_qurry),callback = self.parse_user)


        if 'paging'in results.keys() and results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')
            yield  Request(next_page,callback = self.parse_follows)

    def parse_user(self, response):
        result = json.loads(response.text)
        item = userItem()
        for Filed in item.fields:
            if Filed in result.keys():
                item[Filed] = result.get(Filed)
        yield item

        yield  Request(self.follow_url.format(name = result.get('url_token'),include = self.follow_qurry,offset = 0,limit = 20),callback = self.parse_follows)