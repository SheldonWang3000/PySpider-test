#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2015-06-25 10:08:51
# Project: test

from pyspider.libs.base_handler import *
import re


class Handler(BaseHandler):
    num = 0
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.laho.gov.cn/ywpd/tdgl/zwxx/tdjyxx/gkcy/gkcrgp/index.htm', 
            fetch_type='js', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            if re.match('http://www\.laho\.gov\.cn/ywpd/tdgl/zwxx/tdjyxx/gkcy/gkcrgp/\d+/t\d+_\d+\.htm', each.attr.href, re.U):
                self.crawl(each.attr.href, fetch_type='js', callback=self.content_page)
            if re.match('http://www\.laho\.gov\.cn/ywpd/tdgl/zwxx/tdjyxx/gkcy/gkcrgp/index_\d+\.htm', each.attr.href, re.U):
                self.crawl(each.attr.href, fetch_type='js', callback=self.index_page)

    @config(priority=2)
    def content_page(self, response):
        return {
            "type": 'content',
            "url": response.url,
            "title": response.doc('title').text(),
            "html": response.text,
        }
    
    def on_result(self, result):
        path = 'D:/page/' + str(self.num) + '.txt'
        print type(result)
        if result is not None:
            self.num += 1
            f = open(path, 'wb')
            f.write(result['url'].encode('utf-8'))
            f.close()
        super(Handler, self).on_result(result)
