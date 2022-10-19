import urllib.request

try:
    from pkg_resources import get_distribution
    import pkg_resources.py2_warn
except ImportError:
    pass

import datetime
import json
import re

import PyPDF2
import requests
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import defer
from twisted.internet import reactor

# from under_conn import Mongoconexion

def remove_accents(string):
    # if type(string) is not unicode:
    #     string = unicode(string, encoding='utf-8')

    string = re.sub(u"[àáâãäå]", 'a', string)
    string = re.sub(u"[èéêë]", 'e', string)
    string = re.sub(u"[ìíîï]", 'i', string)
    string = re.sub(u"[òóôõö]", 'o', string)
    string = re.sub(u"[ùúûü]", 'u', string)
    string = re.sub(u"[ýÿ]", 'y', string)
    string = re.sub(u"[ñ]", 'n', string)

    string = re.sub(u"[ÀÁÂÃÄÅ]", 'A', string)
    string = re.sub(u"[ÈÉÊË]", 'E', string)
    string = re.sub(u"[ÌÍÎÏ]", 'I', string)
    string = re.sub(u"[ÒÓÔÕÖ]", 'O', string)
    string = re.sub(u"[ÙÚÛÜ]", 'U', string)
    string = re.sub(u"[ÝŸ]", 'Y', string)
    string = re.sub(u"[Ñ]", 'N', string)

    string = re.sub(u"[()~!@#$%^&*=-]",'',string)
    string = re.sub(u"[\t\n\r]", "", string)

    string = re.sub(u"[-]", "", string)
    return string

class TribunalLaboralEstadoMexicoSpider(scrapy.Spider):
    name = "Tribunal_Laboral_Estado_Mexico"

    # def __init__(self, date, **kwargs):
    #     super().__init__(**kwargs)
    #     self.date = date
    def start_requests(self):
        url = 'http://teca.edomex.gob.mx/boletin_laboral'
        yield scrapy.Request(url=url)
    def parse(self, response, **kwargs):
        for res in response.css('#block-menu-boletin-laboral ul.menu li'):
            url = 'http://teca.edomex.gob.mx'+res.css('a::attr(href)').extract_first()
            yield scrapy.Request(url=url, callback=self.parse_month)
    def parse_month(self, response):
        for res in response.css('.field-item.even p a'):
            link = 'http://teca.edomex.gob.mx'+res.css('::attr(href)').extract_first()
            filename = res.css('::attr(href)').extract_first().split('/')[-1]
            urllib.request.urlretrieve(link,f"D:\\Work\\webscrapers\\scraping\\scraping\\spiders\\Tribunal_Laboral_Estado_Mexico\\{filename}")

            # creating a pdf file object
            pdfFileObj = open(f"D:\\Work\\webscrapers\\scraping\\scraping\\spiders\\Tribunal_Laboral_Estado_Mexico\\{filename}", 'rb')

            # creating a pdf reader object
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            # creating a page object
            pageObj = pdfReader.getPage(0)

            # extracting text from page
            extractedtext = pageObj.extractText()

            date = [v for v in extractedtext.split('\n') if not '  ' == v][1]

            # closing the pdf file object
            pdfFileObj.close()


if __name__ == '__main__':
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(TribunalLaboralEstadoMexicoSpider)
    process.start()
    # configure_logging()
    # runner = CrawlerRunner()
    #
    #
    # @defer.inlineCallbacks
    # def crawl():
    #     with open('dateofnextrun.txt','r',encoding='utf-8') as readdate:
    #         date = readdate.read()
    #     while True:
    #         dateobj = datetime.datetime.strptime(date, '%Y/%m/%d').date()
    #         dateToday = datetime.datetime.today().date()
    #         if dateobj < dateToday:
    #             yield runner.crawl(TribunalLaboralEstadoMéxicoSpider, date)
    #             nextdateobj = dateobj + datetime.timedelta(days=1)
    #             date = nextdateobj.strftime('%Y/%m/%d')
    #             with open('dateofnextrun.txt','w',encoding='utf-8') as writedate:
    #                 writedate.write(date)
    #
    #         else:
    #             break
    #
    #     reactor.stop()
    #
    #
    # crawl()
    # reactor.run()
