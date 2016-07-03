from scrapy.spider import Spider
from scrapy import Request


class TestFilter(Spider):
    start_urls = ['http://nofiht.ml:3289']
    name='demo'
    allowed_domains = ['gov.cn']
    def print_url(self,response):
        print response.url

    def parse(self, response):
        for url in response.xpath('//*[@href]/@href').extract():
            yield Request(url,callback=self.print_url)