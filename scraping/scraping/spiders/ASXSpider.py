import scrapy
import csv
import os
import urllib.request
from scrapy.crawler import CrawlerProcess
import boto3
from botocore.exceptions import NoCredentialsError

ACCESS_KEY = 'access key'
SECRET_KEY = 'secret key'

file = open('ASXListedCompanies.csv', 'r')
input = file.readlines()[3:]
tickers = []
path = os.getcwd()

try:
    p = path + '\PDF'
    os.mkdir(p)
except OSError:
    print("Creation of the directory %s failed" % p)
else:
    print("Successfully created the directory %s " % p)

for inp in input:
    tickers.append(inp.split(',')[1].strip('"'))


class ASXSpider(scrapy.Spider):
    name = 'ASXSpider'
    title = 'asxspider'

    def start_requests(self):
        for ticker in tickers:
            year = 2020
            while year != 2005:
                link = 'https://www.asx.com.au/asx/statistics/announcements.do?by=asxCode&asxCode={}&timeframe=Y&year={}'.format(ticker, year)
                yield scrapy.Request(link, meta={'ticker': ticker, 'year': year})
                year = year - 1

    def parse(self, response):
        try:
            newpath = p + '\{}'.format(response.meta['ticker'])
            os.mkdir(newpath)
        except OSError:
            print("Creation of the directory %s failed" % newpath)
        else:
            print("Successfully created the directory %s " % newpath)

        try:
            newsubpath = newpath + '\{}'.format(response.meta['year'])
            os.mkdir(newsubpath)
        except OSError:
            print("Creation of the directory %s failed" % newsubpath)
        else:
            print("Successfully created the directory %s " % newsubpath)

        for info in response.css('#content > div > announcement_data > table > tbody >tr'):
            item = dict()

            item['ticker'] = response.meta['ticker']
            item['date'] = info.css('td::text').extract_first().strip()
            item['time'] = info.css('td span::text').extract_first().strip()
            if info.css('tr td.pricesens img'):
                item['priceSecs'] = 'yes'
            else:
                item['priceSecs'] = 'no'

            item['headline'] = info.css('td a::text').extract_first().strip()
            pdflink = 'https://www.asx.com.au' + info.css('td a::attr(href)').extract_first()

            yield scrapy.Request(pdflink, callback=self.parsepdf, meta={'item': item, 'path': newsubpath})

    def parsepdf(self, response):
        item = response.meta['item']
        lnk = response.css('body > div > form > input[type=hidden]:nth-child(3)::attr(value)').extract_first()
        lnk = 'https://www.asx.com.au' + lnk

        try:
            urllib.request.urlretrieve(lnk, "{}/file.pdf".format(response.meta['path']))
            item['pdfPath'] = "{}/file.jpg".format(response.meta['path'])
        except:
            try:
                urllib.request.urlretrieve(lnk, "{}/file.pdf".format(response.meta['path']))
                item['pdfPath'] = "{}/file.jpg".format(response.meta['path'])
            except:
                item['pdfPath'] = 'pdf available'

        yield item

    def upload_to_aws(local_file, bucket, s3_file):
        s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                          aws_secret_access_key=SECRET_KEY)

        try:
            s3.upload_file(local_file, bucket, s3_file)
            print("Upload Successful")
            return True
        except FileNotFoundError:
            print("The file was not found")
            return False
        except NoCredentialsError:
            print("Credentials not available")
            return False

    # uploaded = upload_to_aws('local_file', 'bucket_name', 's3_file_name')


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(ASXSpider)
process.start()
