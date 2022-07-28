try:
    from pkg_resources import get_distribution
    import pkg_resources.py2_warn
except ImportError:
    pass

import csv
import json, re
import datetime
from scrapy import Spider
from scrapy import Request
from scrapy.crawler import CrawlerProcess

d = datetime.datetime.now()
d_str = ''.join(str(x) for x in (d.year, d.month, d.day)) + '_' + ''.join(str(x) for x in (d.hour, d.minute, d.second))
Wfile = open('zillowData_{}.csv'.format(d_str), 'w', encoding='utf-8', newline='')
csv_columns = ['Listing type', 'Price', 'Zestimate', 'list price - zestimate', 'Difference in %', 'Time on Zillow',
               'Square feet', 'Year built:', 'Bedrooms', 'Bathrooms', 'Zillow link', 'Address',
               'Type:', 'Lot:', 'Price/sqft:']
writer = csv.DictWriter(Wfile, fieldnames=csv_columns)
writer.writeheader()


class Zillow(Spider):
    name = 'zillow'
    CONCURRENT_REQUESTS = 1
    DOWNLOAD_DELAY = 2
    # meta = {'proxy': 'https://204.12.238.2:19020'},
    # headers = {
    #     'Proxy-Authorization': basic_auth_header(
    #         'nauman.chrom@gmail.com', 'Password123$')
    # }
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Mobile Safari/537.36'
    }

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
        Rfile = open('input_zillow.txt', 'r')
        inputfile = Rfile.read()
        zip_codes = inputfile.split('\n')
        zip_codes = [z for z in zip_codes if z.strip()]
        for zip_code in zip_codes:
            link = zip_code
            # link = f'https://www.zillow.com/homes/{zip_code}_rb/'
            yield Request(link, headers=self.headers, meta={'ziip': zip_code})

    def parse(self, response):
        zip_code = response.meta.get('ziip')
        current_page = response.meta.get('current_page', 1)
        if current_page == 1:
            zip_code = response.meta.get('ziip')
            url = 'https://www.zillow.com/homes/' + zip_code + '_rb/?searchQueryState={"pagination":{},"usersSearchTerm":"' + zip_code + '","mapBounds":{"west":-74.00243523028564,"east":-73.96870376971435,"south":40.70696191540352,"north":40.726068585987996},"regionSelection":[{"regionId":61616,"regionType":7}],"isMapVisible":false,"filterState":{"fsba":{"value":false},"fsbo":{"value":false},"nc":{"value":false},"cmsn":{"value":false},"auc":{"value":false},"fore":{"value":false},"pmf":{"value":false},"pf":{"value":false},"rs":{"value":true}},"isListVisible":true,"mapZoom":15}'
            yield Request(url, headers=self.headers, meta={'current_page': -1})
            try:
                body_data = json.loads('{}:false}}}}'.format(
                    self.get_index(re.findall('<!--{"queryState.+"', response.text), 0).replace('<!--', '')))
                properties = body_data.get('cat1', {}).get('searchResults', {}).get('listResults')
            except:
                return
        else:
            try:
                body_data = json.loads(response.text)
                properties = body_data.get('searchResults', {}).get('listResults', [])
            except:
                return
        if not properties and response.meta.get('tries', 1) < 5:
            tries = response.meta.get('tries', 1) + 1
            yield Request(response.url, headers=self.headers, meta={'current_page': current_page, 'ziip': zip_code,
                                                                    'tries': tries}
                          , dont_filter=True)
            return
        if properties:
            for home in properties:
                data = dict()
                data['Zillow link'] = home['detailUrl']
                data['Price'] = home.get('price', '')
                data['Zestimate'] = home.get('zestimate', '')
                data['Address'] = home.get('address')
                data['Bedrooms'] = home.get('beds')
                data['Bathrooms'] = home.get('baths')
                data['Square feet'] = home.get('area')
                data['Listing type'] = home.get('sgapt')
                data['Time on Zillow'] = home.get('variableData', {}).get('text')
                try:
                    data['list price - zestimate'] = (
                            int(data['Price'].replace('$', '').replace(',', '')) - data['Zestimate']) if data[
                        'Zestimate'] else int(data['Price'].replace('$', '').replace(',', ''))
                except:
                    data['list price - zestimate'] = 0
                data['Difference in %'] = ''
                if data['Zestimate']:
                    data['Difference in %'] = data['list price - zestimate'] / data['Zestimate']
                data['Year built:'] = self.get_dict_value(home, ['hdpData', 'homeInfo', 'yearBuilt'])
                data['Type:'] = self.get_dict_value(home, ['hdpData', 'homeInfo', 'homeType'])
                data['Lot:'] = self.get_dict_value(home, ['hdpData', 'homeInfo', 'lotId64'])
                data['Price/sqft:'] = ''
                if home['area'] and home['unformattedPrice']:
                    data['Price/sqft:'] = home['unformattedPrice'] / home['area']
                # if data['Year built:']:
                writer.writerow(data)
                Wfile.flush()

        if current_page + 1 <= (
                body_data.get('searchList', {}).get('totalPages', 0) or body_data.get('cat1', {}).get('searchList',
                                                                                                      {}).get(
            'totalPages', 0)):
            current_page += 1
            body_data['queryState']['pagination'] = {'currentPage': current_page}
            next_page = f'https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState={body_data["queryState"]}'
            yield Request(next_page, headers=self.headers, meta={'current_page': current_page})

    def get_index(self, data, index):
        if index <= (len(data) - 1):
            return data[index]
        return ''


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(Zillow)
process.start()
