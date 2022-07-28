import csv
import datetime
import json
import re

import csvdiff
import requests
import scrapy
from colour import Color
from scrapy.crawler import CrawlerProcess

'''file for magento'''
priceupdateheaders = ['sku', 'price', 'status', 'store_view_code']
priceupdate = open('cettire_pricelist_magento_temp.csv', 'w', newline='', encoding='utf-8')
pricewriter = csv.DictWriter(priceupdate, fieldnames=priceupdateheaders)
pricewriter.writeheader()

'''file for pricelist'''
pricelistheaders = ['GROUP SKU', 'PRODUCT SKU', 'RETAIL PRICE', 'WEBSITES']
pricelistfile = open('cettire_pricelist_odoo_temp.csv', 'w', newline='', encoding='utf-8')
pricelistwriter = csv.DictWriter(pricelistfile, fieldnames=pricelistheaders)
pricelistwriter.writeheader()

# '''file for Scraping Data'''
# scrapingdataheaders = ['SR. NO', 'PRODUCT TYPE', 'GROUP SKU', 'VARIATION TYPE', 'PRODUCT SKU', 'UPC/EAN', 'BRAND', 'NAME', 'ORIGINAL PRICE', 'KSA PRICE', 'RETAIL PRICE', 'WHOLESALE PRICE', 'DESCRIPTION', 'MAINPICTURE', 'PICTURE1', 'PICTURE2', 'PICTURE3', 'PICTURE4', 'PICTURE5', 'GENDER', 'MAIN CATEGORY', 'CATEGORY', 'SUB CATEGORY', 'CATEGORIES', 'SIZE', 'COLOR', 'MATERIAL', 'ORIGIN', 'SIZE SLUG', 'DESCRIPTION PLAIN', 'DELIVERY_INFORMATION', 'RESTRICT_PAYMENT', 'META KEYWORDS (EN)', 'META TITLE (EN)', 'META DESCRIPTION (EN)', 'BADGES', 'ADDITIONAL CATEGORIES', 'SEARCH TERMS', 'BARCODE']
# scrapingdatafile = open('cettire_scrapingdata.csv', 'w', newline='', encoding='utf-8')
# scrapingdatawriter = csv.DictWriter(scrapingdatafile, fieldnames=scrapingdataheaders)
# scrapingdatawriter.writeheader()

ct = datetime.datetime.now()
TS = str(ct.timestamp()).replace('.', '')
# fileout = open('cettire.csv', 'w', newline='', encoding='utf-8')
# writer = csv.DictWriter(fileout, fieldnames=headers_csv)
# writer.writeheader()
headers = {
    "Connection": "keep-alive",
    "sec-ch-ua": "\"Chromium\";v=\"92\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"92\"",
    "accept": "application/json",
    "DNT": "1",
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "content-type": "application/x-www-form-urlencoded",
    "Origin": "https://www.cettire.com",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://www.cettire.com/",
    "Accept-Language": "en-US,en;q=0.9"
}

menshoesbody = '{"requests":[{"indexName":"dev_Cettire_date_desc","params":"query=&hitsPerPage=48&maxValuesPerFacet=20000&page=0&distinct=1&facets=%5B%22tags%22%2C%22Color%22%2C%22Size%22%2C%22vendor%22%2C%22product_type%22%5D&tagFilters=&facetFilters=%5B%22visibility%3AYES%22%2C%22department%3Amen%22%2C%22tags%3AShoes%22%2C%5B%22product_type%3ASneakers%22%5D%5D"},{"indexName":"dev_Cettire_date_desc","params":"query=&hitsPerPage=1&maxValuesPerFacet=20000&page=0&distinct=1&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&analytics=false&clickAnalytics=false&facets=%5B%22product_type%22%5D&facetFilters=%5B%22visibility%3AYES%22%2C%22department%3Amen%22%2C%22tags%3AShoes%22%5D"}]}'
womenshoesbody = '{"requests":[{"indexName":"dev_Cettire_date_desc","params":"query=&hitsPerPage=48&maxValuesPerFacet=20000&page=0&distinct=1&facets=%5B%22tags%22%2C%22Color%22%2C%22Size%22%2C%22vendor%22%2C%22product_type%22%5D&tagFilters=&facetFilters=%5B%22visibility%3AYES%22%2C%22department%3Awomen%22%2C%22tags%3AShoes%22%2C%5B%22product_type%3ASneakers%22%5D%5D"},{"indexName":"dev_Cettire_date_desc","params":"query=&hitsPerPage=1&maxValuesPerFacet=20000&page=0&distinct=1&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&analytics=false&clickAnalytics=false&facets=%5B%22product_type%22%5D&facetFilters=%5B%22visibility%3AYES%22%2C%22department%3Awomen%22%2C%22tags%3AShoes%22%5D"}]}'
womenbagbody = '{"requests":[{"indexName":"dev_Cettire_date_desc","params":"query=&hitsPerPage=48&maxValuesPerFacet=20000&page=0&distinct=1&facets=%5B%22tags%22%2C%22Color%22%2C%22Size%22%2C%22vendor%22%2C%22product_type%22%5D&tagFilters=&facetFilters=%5B%22visibility%3AYES%22%2C%22department%3Awomen%22%2C%22tags%3ABags%22%5D"}]}'
menbagbody = '{"requests":[{"indexName":"dev_Cettire_date_desc","params":"query=&hitsPerPage=48&maxValuesPerFacet=20000&page=0&distinct=1&facets=%5B%22tags%22%2C%22Color%22%2C%22Size%22%2C%22vendor%22%2C%22product_type%22%5D&tagFilters=&facetFilters=%5B%22visibility%3AYES%22%2C%22department%3Amen%22%2C%22tags%3ABags%22%5D"}]}'
# vendor = 1482
processed = []


def check_color(color):
    try:
        # Converting 'deep sky blue' to 'deepskyblue'
        color = color.replace(" ", "")
        Color(color)
        # if everything goes fine then return True
        return True
    except ValueError:  # The color code was not found
        return False


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


class cettire(scrapy.Spider):
    name = 'cettire'

    def start_requests(self):
        url = 'https://6l0oqj41cq-2.algolianet.com/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20vanilla%20JavaScript%20(lite)%203.27.1%3Binstantsearch.js%201.12.1%3BJS%20Helper%202.26.0&x-algolia-application-id=6L0OQJ41CQ&x-algolia-api-key=ee556f77348dacc02278dafa57be6d34'

        '''for mens shoes'''
        res = requests.post(url=url, headers=headers, data=menshoesbody)
        jsondata = json.loads(res.content.decode('utf-8'))
        totalpagesmenshoes = jsondata['results'][0]['nbPages']
        i = 0
        while i <= totalpagesmenshoes:
            newmenshoesbody = menshoesbody.split('page=0')[0] + f'page={i}' + menshoesbody.split('page=0')[
                1] + f'page={i}' + \
                              menshoesbody.split('page=0')[2]
            i += 1
            yield scrapy.Request(url=url, method='POST', headers=headers, body=newmenshoesbody,
                                 meta={'maincategory': 'Men', 'category': 'Shoes'})

        '''for womens shoes'''
        res = requests.post(url=url, headers=headers, data=womenshoesbody)
        jsondata = json.loads(res.content.decode('utf-8'))
        totalpageswomenshoes = jsondata['results'][0]['nbPages']
        i = 0
        while i <= totalpageswomenshoes:
            newwomenshoesbody = womenshoesbody.split('page=0')[0] + f'page={i}' + womenshoesbody.split('page=0')[
                1] + f'page={i}' + womenshoesbody.split('page=0')[2]
            i += 1
            yield scrapy.Request(url=url, method='POST', headers=headers, body=newwomenshoesbody,
                                 meta={'maincategory': 'Women', 'category': 'Shoes'})

        '''for Mens Bags'''
        res = requests.post(url=url, headers=headers, data=menbagbody)
        jsondata = json.loads(res.content.decode('utf-8'))
        totalpagesmenbag = jsondata['results'][0]['nbPages']
        i = 0
        while i <= totalpagesmenbag:
            newmenbagbody = menbagbody.split('page=0')[0] + f'page={i}' + menbagbody.split('page=0')[1]
            i += 1
            yield scrapy.Request(url=url, method='POST', headers=headers, body=newmenbagbody,
                                 meta={'maincategory': 'Men', 'category': 'Bags'})

        '''for womens Bags'''
        res = requests.post(url=url, headers=headers, data=womenbagbody)
        jsondata = json.loads(res.content.decode('utf-8'))
        totalpageswomenbag = jsondata['results'][0]['nbPages']
        i = 0
        while i <= totalpageswomenbag:
            newwomenbagbody = womenbagbody.split('page=0')[0] + f'page={i}' + womenbagbody.split('page=0')[1]
            i += 1
            yield scrapy.Request(url=url, method='POST', headers=headers, body=newwomenbagbody,
                                 meta={'maincategory': 'Women', 'category': 'Bags'})

    def parse(self, response, **kwargs):
        data = json.loads(response.text)
        for dt in data['results'][0]['hits']:
            if not dt["handle"]:
                continue
            url = f'https://www.cettire.com/products/{dt["handle"]}'
            yield scrapy.Request(url, callback=self.parse_data, meta={'data': dt, 'maincategory': response.meta['maincategory'], 'category': response.meta['category']})

    def parse_data(self, response):
        dt = response.meta['data']
        item = dict()
        item['ref'] = TS
        jsonstringforsizes = [v for v in response.css('script::text').extract() if 'theme.productSingleObject =' in v][0].split('theme.productSingleObject = ')[-1].split(';')[0]
        try:
            jsfs = json.loads(jsonstringforsizes)
        except:
            jsonstringforsizes = [v for v in response.css('script::text').extract() if 'theme.productSingleObject =' in v][0].split('theme.productSingleObject =')[-1].split('};')[0] + '}'
            jsfs = json.loads(jsonstringforsizes)
        item['original_price'] = jsfs['price'] / 100
        item['serial_no'] = str(dt['product_id']) + 'AED'
        item['whole_sale_price'] = jsfs['price'] / 100
        item['retail_price'] = jsfs['price'] / 100
        try:
            item['strike_through_price'] = jsfs['compare_at_price'] / 100
        except:
            pass
        item['name_en'] = dt['title']
        item['brand'] = dt['vendor']
        item['gender'] = ' || '.join(dt['department'])
        rss = scrapy.Selector(text=dt['body_html'])
        item['description_en'] = ' '.join(rss.css('html ::text').extract())
        item['description_plain_en'] = ' '.join(rss.css('html ::text').extract())
        item['url_key'] = response.url
        item['main_category'] = response.meta['maincategory']
        item['category'] = response.meta['category']
        item['sub_category'] = dt['product_type']
        item['base_category'] = item['main_category'] + '/' + item['category'] + '/' + item['sub_category']
        try:
            item['color'] = dt['Color']
        except:
            item['color'] = ''
        if item['color'] == 'multi' or item['color'] == 'Multi':
            item['group_sku'] = str(jsfs['id']) + '-Multicolor'
        else:
            item['group_sku'] = str(jsfs['id']) + '-' + item['color'].title()
        item['origin'] = 'website'
        try:
            item['size_slug'] = [re.findall(r'(\w+?)(\d+)', dt['Size'])[0]][0][0]
        except:
            item['size_slug'] = dt['Size']
        item['delivery_information'] = '15 to 20 days'
        item['main_pic'] = jsfs['images'][0]
        for i, img in enumerate(jsfs['images']):
            if i > 36:
                break
            item[f'pic_{i + 1}'] = img

        index = 0
        if 'Bag' in response.meta['category']:
            for sz in jsfs['variants']:
                index += 1
                item['variant_{}'.format(index)] = sz['option2']
                item['variant_{}_price'.format(index)] = int(sz['price'] / 100)
                if sz['inventory_quantity'] == 0:
                    item['variant_{}_stock'.format(index)] = 'Out Of Stock'
                else:
                    item['variant_{}_stock'.format(index)] = sz['inventory_quantity']

                for i in range(0, 3):
                    PUitem = dict()
                    PUitem['sku'] = item['group_sku'] + '-OS'  # + item['variant_{}'.format(index)]
                    if i == 0:
                        PUitem['store_view_code'] = 'en'
                        PUitem['price'] = int((30 + (1.13 * item['variant_{}_price'.format(index)])) * 3.95)  # (50 + (item['variant_{}_price'.format(index)] * 1.13)) * 4.86
                        PUitem['status'] = 1
                        if item['variant_{}_price'.format(index)] == 0:
                            PUitem['price'] = 0
                            PUitem['status'] = 2

                    elif i == 1:
                        PUitem['store_view_code'] = 'sa_en'
                        PUitem['price'] = int(((((30 + (1.13 * item['variant_{}_price'.format(index)])) * 3.95) * 10) / 100) + (30 + (1.13 * item['variant_{}_price'.format(index)])) * 3.95)
                        PUitem['status'] = 1
                        if item['variant_{}_price'.format(index)] == 0:
                            PUitem['price'] = 0
                            PUitem['status'] = 2
                    elif i == 2:
                        PUitem['store_view_code'] = 'us_en'
                        PUitem['price'] = int(item['variant_{}_price'.format(index)])
                        PUitem['status'] = 1
                        if item['variant_{}_price'.format(index)] == 0:
                            PUitem['price'] = 0
                            PUitem['status'] = 2
                    pricewriter.writerow(PUitem)
                    priceupdate.flush()

                PLitem = dict()

                PLitem['GROUP SKU'] = item['group_sku']
                PLitem['PRODUCT SKU'] = item['group_sku'] + '-OS'  # + item['variant_{}'.format(index)]
                PLitem['RETAIL PRICE'] = int((30 + (1.13 * item['variant_{}_price'.format(index)])) * 3.95)
                if item['variant_{}_price'.format(index)] == 0:
                    PLitem['RETAIL PRICE'] = 0
                PLitem['WEBSITES'] = 'United Arab Emirates'
                pricelistwriter.writerow(PLitem)
                pricelistfile.flush()

        else:
            for sz in jsfs['variants']:
                index += 1
                if 'IT/FR' in sz['option1']:
                    item['variant_{}'.format(index)] = ''.join(list(sz['option1'])[5:])
                else:
                    item['variant_{}'.format(index)] = ''.join(list(sz['option1'])[2:])
                item['variant_{}_price'.format(index)] = int(sz['price'] / 100)
                if sz['inventory_quantity'] == 0:
                    item['variant_{}_stock'.format(index)] = 'Out Of Stock'
                else:
                    item['variant_{}_stock'.format(index)] = sz['inventory_quantity']

                for i in range(0, 3):
                    PUitem = dict()
                    PUitem['sku'] = item['group_sku'] + '-' + item['variant_{}'.format(index)]
                    if i == 0:
                        PUitem['store_view_code'] = 'en'
                        PUitem['price'] = int((30 + (1.13 * item['variant_{}_price'.format(index)])) * 3.95)
                        PUitem['status'] = 1
                        if item['variant_{}_stock'.format(index)] == 'Out Of Stock':
                            PUitem['price'] = 0
                            PUitem['status'] = 2

                    elif i == 1:
                        PUitem['store_view_code'] = 'sa_en'
                        PUitem['price'] = int(((((30 + (1.13 * item['variant_{}_price'.format(index)])) * 3.95) * 10) / 100) + (30 + (1.13 * item['variant_{}_price'.format(index)])) * 3.95)
                        PUitem['status'] = 1
                        if item['variant_{}_stock'.format(index)] == 'Out Of Stock':
                            PUitem['price'] = 0
                            PUitem['status'] = 2
                    elif i == 2:
                        PUitem['store_view_code'] = 'us_en'
                        PUitem['price'] = int(item['variant_{}_price'.format(index)])
                        PUitem['status'] = 1
                        if item['variant_{}_stock'.format(index)] == 'Out Of Stock':
                            PUitem['price'] = 0
                            PUitem['status'] = 2
                    pricewriter.writerow(PUitem)
                    priceupdate.flush()

                PLitem = dict()

                PLitem['GROUP SKU'] = item['group_sku']
                PLitem['PRODUCT SKU'] = item['group_sku'] + '-' + item['variant_{}'.format(index)]
                PLitem['RETAIL PRICE'] = int((30 + (1.13 * item['variant_{}_price'.format(index)])) * 3.95)
                if item['variant_{}_stock'.format(index)] == 'Out Of Stock':
                    PLitem['RETAIL PRICE'] = 0
                PLitem['WEBSITES'] = 'United Arab Emirates'
                pricelistwriter.writerow(PLitem)
                pricelistfile.flush()
        processed.append(item)

    def close(spider, reason):
        priceupdate.close()
        pricelistfile.close()
        diffmagento = csvdiff.diff_files("cettire_pricelist_magento_original.csv", "cettire_pricelist_magento_temp.csv", ['sku', 'store_view_code'])
        '''delta file for magento'''
        deltaupdateheaders = ['sku', 'price', 'status', 'store_view_code']
        deltapriceupdate = open('cettire_pricelist_magento_delta.csv', 'w', newline='', encoding='utf-8')
        deltapricewriter = csv.DictWriter(deltapriceupdate, fieldnames=deltaupdateheaders)
        deltapricewriter.writeheader()

        originalpriceupdate = open('cettire_pricelist_magento_original.csv', 'a+', newline='', encoding='utf-8')
        originalpriceupdatewriter = csv.DictWriter(originalpriceupdate, fieldnames=deltaupdateheaders)

        removed = []
        for item in diffmagento['removed']:
            item__ = dict()
            item__['sku'] = item['sku']
            item__['store_view_code'] = item['store_view_code']
            item__['status'] = '2'
            item__['price'] = 0
            deltapricewriter.writerow(item__)
            deltapriceupdate.flush()
            removed.append(item__)

        for added in diffmagento['added']:
            deltapricewriter.writerow(added)
            originalpriceupdatewriter.writerow(added)
            originalpriceupdate.flush()
            deltapriceupdate.flush()
        change = []
        for changed in diffmagento['changed']:
            chang = dict()
            chang['sku'] = changed['key'][0]
            try:
                chang['price'] = int(float(changed['fields']['price']['to']))
                if changed['fields']['price']['to'] != '0':
                    chang['status'] = '1'
                else:
                    chang['status'] = '2'
            except:
                chang['status'] = changed['fields']['status']['to']
                if chang['status'] == '2':
                    chang['price'] = '0'
            chang['store_view_code'] = changed['key'][-1]
            deltapricewriter.writerow(chang)
            deltapriceupdate.flush()
            change.append(chang)
        # os.remove("cettire_pricelist_magento_original.csv")
        # os.rename('cettire_pricelist_magento_temp.csv', 'cettire_pricelist_magento_original.csv')

        original_list = list(csv.DictReader(open('cettire_pricelist_magento_original.csv')))
        originalpriceupdate = open('cettire_pricelist_magento_original.csv', 'w', newline='', encoding='utf-8')
        originalpriceupdatewriter = csv.DictWriter(originalpriceupdate, fieldnames=deltaupdateheaders)
        originalpriceupdatewriter.writeheader()
        finalChangeslist = change + removed
        for o_item in original_list:
            for c_item in finalChangeslist:
                if o_item['sku'] == c_item['sku'] and o_item['store_view_code'] == c_item['store_view_code']:
                    o_item['price'] = int(c_item['price'])
                    o_item['status'] = c_item['status']

            originalpriceupdatewriter.writerow(o_item)
            originalpriceupdate.flush()

        '''delta file for pricelist'''
        diffpricelist = csvdiff.diff_files('cettire_pricelist_odoo_original.csv', 'cettire_pricelist_odoo_temp.csv', ['GROUP SKU', 'PRODUCT SKU', 'WEBSITES'])
        deltapricelistheaders = ['GROUP SKU', 'PRODUCT SKU', 'RETAIL PRICE', 'WEBSITES']
        deltapricelistfile = open('cettire_pricelist_odoo_delta.csv', 'w', newline='', encoding='utf-8')
        deltapricelistwriter = csv.DictWriter(deltapricelistfile, fieldnames=deltapricelistheaders)
        deltapricelistwriter.writeheader()

        originalpricelist = open('cettire_pricelist_odoo_original.csv', 'a+', newline='', encoding='utf-8')
        originalpricelistwriter = csv.DictWriter(originalpricelist, fieldnames=deltapricelistheaders)

        removed = []
        for item in diffpricelist['removed']:
            item__ = dict()
            item__['GROUP SKU'] = item['GROUP SKU']
            item__['PRODUCT SKU'] = item['PRODUCT SKU']
            item__['RETAIL PRICE'] = 0
            item__['WEBSITES'] = item['WEBSITES']
            deltapricelistwriter.writerow(item__)
            deltapricelistfile.flush()
            removed.append(item__)

        for added in diffpricelist['added']:
            deltapricelistwriter.writerow(added)
            originalpricelistwriter.writerow(added)
            originalpricelist.flush()
            deltapricelistfile.flush()
        change = []
        for changed in diffpricelist['changed']:
            chng = dict()
            chng['PRODUCT SKU'] = changed['key'][1]
            chng['GROUP SKU'] = changed['key'][0]
            chng['RETAIL PRICE'] = int(float(changed['fields']['RETAIL PRICE']['to']))
            chng['WEBSITES'] = changed['key'][2]

            deltapricelistwriter.writerow(chng)
            deltapricelistfile.flush()
            change.append(chng)

        original_list = list(csv.DictReader(open('cettire_pricelist_odoo_original.csv')))
        originalpriceupdate = open('cettire_pricelist_odoo_original.csv', 'w', newline='', encoding='utf-8')
        originalpriceupdatewriter = csv.DictWriter(originalpriceupdate, fieldnames=deltapricelistheaders)
        originalpriceupdatewriter.writeheader()

        finalChangeslist = change + removed
        for o_item in original_list:
            for c_item in finalChangeslist:
                if o_item['PRODUCT SKU'] == c_item['PRODUCT SKU']:
                    o_item['RETAIL PRICE'] = int(float(c_item['RETAIL PRICE']))
            originalpriceupdatewriter.writerow(o_item)
            originalpriceupdate.flush()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(cettire)
process.start()