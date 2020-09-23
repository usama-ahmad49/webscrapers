import csv
import datetime
import os

import requests
import scrapy

from scraping import settings
from scraping.spiders.base_spider import BaseSpider

csv_columns = ['hotelName', 'hotelId', 'roomName', 'roomId', 'Sleeps', 'CheckIn', 'CheckOut', 'price',
               'breakfast', 'freeCancellation', 'prepayment']
csvfile = open('booking.csv', 'w', newline='', encoding="utf-8")
writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
writer.writeheader()


class Booking(BaseSpider):
    name = 'booking'
    title = 'Booking'
    use_selenium = True
    start_urls = []
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': settings.DOWNLOADER_MIDDLEWARES
    }
    url = '{}?lang=en-gb;checkin={};checkout={};group_adults=2;group_children=0;lang_changed=1;selected_currency=EUR'

    urls = ['https://www.booking.com/hotel/it/garni-villa-gloria.it.html',
            'https://www.booking.com/hotel/it/eco-bonapace.it.html',
            'https://www.booking.com/hotel/it/holiday.it.html']
    google_sheet = ('https://docs.google.com/spreadsheets/d/1S12E7PcemxlgUpEODfr-VwVygDh2bPtjTArV24hE2Mc/export?'
                    'format=csv&id=1S12E7PcemxlgUpEODfr-VwVygDh2bPtjTArV24hE2Mc&gid=0')

    @staticmethod
    def get_dict_value(data, key_list, default=''):
        """
        gets a dictionary and key_list, apply key_list sequentially on dictionary and return value
        :param data: dictionary
        :param key_list: list of key
        :param default: return value if key not found
        :return:
        """
        for key in key_list:
            if data and isinstance(data, dict):
                data = data.get(key, default)
            else:
                return default
        return data

    def start_requests(self):
        today = datetime.datetime.now().date()
        google_sheet_url = self.google_sheet
        response = requests.get(google_sheet_url)
        pages = [link.replace(',', '') for link in response.content.decode('utf-8').split()]

        for hotel_url in pages:
            for i in range(1, 90):
                check_in = (today + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
                check_out = (today + datetime.timedelta(days=i + 1)).strftime("%Y-%m-%d")
                # print(self.url.format(hotel_url, check_in, check_out))
                yield scrapy.Request(self.url.format(hotel_url, check_in, check_out),
                                     # yield scrapy.Request('https://www.booking.com/hotel/it/eco-bonapace.it.html
                                     # ?checkin=2020-07-11;checkout=2020-07-12;group_adults=2;group_children=0',
                                     meta={'js': True, 'check_in': check_in,
                                           'check_out': check_out}, dont_filter=True)

    def parse(self, response):
        for room in response.css('.hprt-table tr'):
            if room.css('::attr(data-block-id)'):
                item = dict()
                item['hotelName'] = response.css('h2.hp__hotel-name ::text').extract()[-1].strip() if response.css(
                    'h2.hp__hotel-name ::text').extract() else None
                item['hotelId'] = room.css('::attr(data-block-id)').extract_first('').split('_')[1]
                item['roomId'] = room.css('::attr(data-block-id)').extract_first('').split('_')[0]
                room_id = '{}_{}_2_1_0'.format(item['roomId'], item['hotelId'])
                item['roomName'] = response.css('a[data-room-id="{}"] span::text'.format(item['roomId'])).extract_first(
                    '').strip()
                item['Sleeps'] = len(room.css('.bicon.bicon-occupancy'))
                # item['URL'] = response.url
                item['CheckIn'] = response.meta['check_in']
                item['CheckOut'] = response.meta['check_out']
                item['price'] = room.css('.bui-price-display__value ::text').extract_first('').strip()
                item['breakfast'] = 'included' if 'breakfast' in ''.join(room.css(
                    '.hprt-green-condition.jq_tooltip.rt_clean_up_options ::text').extract()) else 'not included'
                item['freeCancellation'] = 'yes' if room.css('.e2e-free-cancellation') else 'no'
                item['prepayment'] = 'no' if room.css('.e2e-no-prepayment.hprt-green-condition') else 'yes'
                writer.writerow(item)
                csvfile.flush()
                yield item

    def spider_closed(self, spider):
        url = 'http://178.62.193.245/upload.php'
        headers = {
            'X-API-KEY': 'fC3v88BMNXmrNHjmX48m8HxUx9PHT2Cy',
            'Accept': 'application/json'
        }
        day = '0'+str(datetime.datetime.now().day) if len(str(datetime.datetime.now().day))==1 else datetime.datetime.now().day
        month = '0'+str(datetime.datetime.now().month) if len(str(datetime.datetime.now().month))==1 else datetime.datetime.now().month
        year = str(datetime.datetime.now().year)[:2]
        data = {
            'partnerId': 'booking_scraper',
            'date': '{}{}{}'.format(day, month, year)
        }

        files = {'file': open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'booking.csv'))}
        requests.post(url, headers=headers, data=data, files=files)
