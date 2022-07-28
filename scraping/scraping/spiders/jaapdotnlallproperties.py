import urllib.request

import mysql.connector
import scrapy
from scrapy.crawler import CrawlerProcess
from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods import media

mydb = mysql.connector.connect(
    host="127.0.0.1",
    password="123456789",
    user="root",
    database="testfloderschema"
)
mycursor = mydb.cursor()

client = Client('https://realzz.nl/xmlrpc.php', 'realzz', '!Realzz@2020!')


class jaapdonlallproperties(scrapy.Spider):
    name = 'jaapdonlallproperties'

    def start_requests(self):
        yield scrapy.Request(url='https://www.jaap.nl/bladeren', callback=self.parse_pages)

    def parse_pages(self, response):
        for prop_url in response.css('.detailblock-header a'):
            p_url = 'https://www.jaap.nl{}'.format(prop_url.css('::attr(href)').extract_first())
            yield scrapy.Request(url=p_url, callback=self.parse_province)

    def parse_province(self, response):
        totalpagestext = [v for v in response.css('.detailblock-header::text').extract() if '\r\n' not in v]
        for i, province in enumerate(response.css('.detailblock-header a')):
            total_props = int((totalpagestext[i]).strip().replace('(', '').replace(')', ''))
            pg = total_props / 30
            if pg - int(pg) == 0:
                t_p = int(pg)
            else:
                t_p = int(pg) + 1
            counter = 1
            while counter <= t_p:
                prov_url = 'https://www.jaap.nl' + province.css('::attr(href)').extract_first() + f'/p{counter}'
                counter = counter + 1
                yield scrapy.Request(url=prov_url, callback=self.parse_ind_url)

    def parse_ind_url(self, response):
        for resp in response.css('.property-list .property a.property-inner'):
            url = resp.css('::attr(href)').extract_first()
            yield scrapy.Request(url=url, callback=self.parse_property)

    def parse_property(self, response):
        number = 1
        streetAddress = response.css('.detail-address .detail-address-street::text').extract_first()
        zipCityAddress = response.css('.detail-address .detail-address-zipcity::text').extract_first()
        price = response.css('.detail-address .detail-address-price::text').extract_first().strip()
        try:
            image = '\n'.join(v for v in response.css('.carousel-inner .item img::attr(data-lazy-load-src)').extract() if 'https://' in v)
            image_url = response.css('.carousel-inner .item img::attr(data-lazy-load-src)').extract_first()
        except:
            image = response.css('.carousel-inner img::attr(data-lazy-load-src)').extract_first('')
            image_url = image
        description = (''.join(v for v in response.css('#long-description ::text').extract() if '\r\n' not in v if v not in '\r')).replace('\r', '')
        if description == '':
            description = response.css('.short-description ::text').extract_first('').strip()
        for prop in response.css('.detail-tab-content.kenmerken table'):
            for prop1 in prop.css('tr'):
                if prop1.css('td.name .no-dots::text').extract_first():
                    continue
                if 'Type' in prop1.css('td.name .no-dots::text').extract_first():
                    type = prop1.css('td.value ::text').extract_first().split()
                if 'Perceeloppervlakte' in prop1.css('td.name .no-dots::text').extract_first():
                    area = int(prop1.css('td.value ::text').extract_first().split().split()[0].replace(',', ''))
                if 'Bouwjaar' in prop1.css('td.name .no-dots::text').extract_first():
                    constructionYear = prop1.css('td.value ::text').extract_first().split()
                if 'Energielabel' in prop1.css('td.name .no-dots::text').extract_first():
                    Energylabel = prop1.css('td.value ::text').extract_first().split()
                if 'Kamers' in prop1.css('td.name .no-dots::text').extract_first():
                    Rooms = prop1.css('td.value ::text').extract_first().split()
                if 'Slaapkamers' in prop1.css('td.name .no-dots::text').extract_first():
                    Bedrooms = prop1.css('td.value ::text').extract_first().split()
                if 'Sanitaire voorzieningen' in prop1.css('td.name .no-dots::text').extract_first():
                    washroom = prop1.css('td.value ::text').extract_first().split()
                if 'Keuken' in prop1.css('td.name .no-dots::text').extract_first():
                    kitchen = prop1.css('td.value ::text').extract_first().split()

        filename = f'E:\Project\pricescraperlk\scraping\scraping\spiders\jappnlimages\{streetAddress}.jpg'
        urllib.request.urlretrieve(image_url, filename)
        data = {
            'name': f'{streetAddress}.jpg',
            'type': 'image/jpeg',  # mimetype
        }
        with open(filename, 'rb') as img:
            data['bits'] = xmlrpc_client.Binary(img.read())
        client.call(media.UploadFile(data))
        data = (number, streetAddress, zipCityAddress, price, image, description, type, area, constructionYear, Energylabel, Rooms, Bedrooms, washroom, kitchen)
        query = "insert into jaapnl (number, streetAddress, zipCityAddress, price, image, description, type,area,constructionYear,Energylabel,Rooms,Bedrooms,washroom,kitchen) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        mycursor.execute(query, data)
        mydb.commit()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(jaapdonlallproperties)
process.start()
