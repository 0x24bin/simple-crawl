#!/usr/bin/env python
#coding:utf-8
"""
  Author:  fiht --<fiht@qq.com>
  Purpose: 增量式爬取网站
  Created: 2016年06月20日
"""
import geoip2.database
import scrapy
from bs4 import BeautifulSoup
import requests
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
            result = ip_database.country(ip).country.name=='China'
        except Exception:
            return False
    #----------------------------------------------------------------------
    @staticmethod
    def canCrawl(url):
        """给一个url返回可不可以抓取,依赖全局变量"""
        if 'http' not in url:
            return False
        netloc = urlparse(url)[1]
        if netloc in url_set:
            return False
        try:
            ip = socket.gethostbyname(netloc)
            #print('%s---->%s'%(url,ip))
        except Exception:
            return False # 找不到IP 返回false
        return Util.ip_isChina(ip)
    #----------------------------------------------------------------------
    @staticmethod
    def add_toInjection(url,netloc=None):
        """每个主机只取一个链接,如果显式地传入了netloc参数,则xxxx"""
        if netloc:
            return netloc not in sqlInjection_set
        return urlparse(url)[1] not in sqlInjection_set
########################################################################
class test(scrapy.spiders.Spider):
    """test Demo"""
    name = 'main'
    start_urls = ['http://www.bkjx1.sdu.edu.cn']
    #----------------------------------------------------------------------
    def parse(self,response):
        """parse"""
        soup = BeautifulSoup(response.body,'lxml')
        #print(soup.prettify())
        for i in soup.findAll('a'):
            if i.has_attr('href'):
                url = i['href']
                #print(url)
                if Util.canCrawl(url):
                    url_set.add(urlparse(url)[1])
#                    print('返回一个等待抓取的链接%s'%url)
                    yield scrapy.Request(url)
                if '=' in url:
                    if 'http' not in url:
                        url = urlparse(response.url)[1]+'/'+'url'
                    if Util.add_toInjection(url):
                        print('等待抓取的注入点%s'%url)
                        sqlInjection_set.add(urlparse(url)[1])