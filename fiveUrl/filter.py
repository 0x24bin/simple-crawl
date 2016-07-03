from scrapy.dupefilters import RFPDupeFilter
from scrapy.utils.request import request_fingerprint
from urlparse import urlparse


class CustomFilter(RFPDupeFilter):

    def __getid(self,url):
        mm = urlparse(url)[1]
        print '------>',mm
        return mm

    def request_seen(self, request):
        fp = self.__getid(request.url)
        print '9999',fp
        print 'self.fingerprints',self.fingerprints
        if fp in self.fingerprints:
            return True
        self.fingerprints.add(fp)
