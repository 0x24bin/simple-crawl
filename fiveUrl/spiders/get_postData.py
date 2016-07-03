#!/usr/bin/env python
#coding:utf-8
"""
  Author:  fiht --<fiht@qq.com>
  Purpose: 增量式爬取网站
  Created: 2016年06月20日
"""
import geoip2.database
import scrapy
from fiveUrl.items import FiveurlItem
import socket
from urlparse import urlparse
url_set = set()
sqlInjection_set = set()
ip_database = geoip2.database.Reader('../1.mmdb')
########################################################################
class Util:
    """工具类"""
    #----------------------------------------------------------------------
    @staticmethod
    #----------------------------------------------------------------------
    def ip_isChina(ip):
        """本地的数据"""
        try:
            result = ip_database.country(socket.gethostbyname(ip)).country.name=='China'
        except Exception:
            return False
        return result
    #----------------------------------------------------------------------
    @staticmethod
    def canCrawl(url):
        """给一个url返回可不可以抓取,依赖全局变量"""
        if 'http' not in url:
            return False
        netloc = urlparse(url)[1]
        if netloc in url_set: #or 'gov.cn' not in netloc:
            return False
        return True #不对ip进行检验
        return Util.ip_isChina(ip)
    #----------------------------------------------------------------------
    @staticmethod
    def add_toInjection(url,netloc=None):
        """每个主机只取一个链接,如果显式地传入了netloc参数,则xxxx"""
        if netloc:
            return netloc not in sqlInjection_set
        things = urlparse(url)
        if things[1]+things[2] not in sqlInjection_set:
            sqlInjection_set.add(things[1]+things[2])
            return True
    #----------------------------------------------------------------------
    @staticmethod
    def get_postdata(response):
        """给一个小的response对象，返回url和要post的数据"""
        url = response.xpath('@action').extract()
        data = ''
        print(response.xpath('input[@type!="submit"]/@name').extract())
        for i in response.xpath('input[@type!="submit"]/@name').extract():
            data+=i+'=&'
        return url,data[:-1]
########################################################################
class test(scrapy.spiders.Spider):
    """test Demo"""
    name = 'demo'
    start_urls = ['http://emec.nenu.edu.cn:8088/emec/pages/index/IndexAction.do?action=index']
 #   start_urls = ['http://%s'%i.strip() for i in open('target')]
#    allowed_domains = ['gov.cn']
    #----------------------------------------------------------------------
    def parse(self,response):
        """parse"""
        #print(soup.prettify())
        for form in response.xpath('//form[@method="post"]'):
            #print(url)
            # 全是post表格
            print(Util.get_postdata(form))
            # if Util.canCrawl(url):
                # url_set.add(urlparse(url)[1])
# #                    print('返回一个等待抓取的链接%s'%url)
                # #yield scrapy.Request(url, priority=-20)
            # if '=' in url and 'css' not in url:
    # #                   print url
                # if 'http' not in url:
                    # url = 'http://'+urlparse(response.url)[1]+'/'+url
                # if Util.add_toInjection(url):
                    # #print('等待抓取的注入点%s'%url)
                    # item = FiveurlItem()
                    # item['url'] = url
                    # item['hasScaned'] = 0
                    # yield item
