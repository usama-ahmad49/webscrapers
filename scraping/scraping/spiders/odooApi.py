import json
import logging
import xmlrpc.client
import requests
import time
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

outputlogfile = open('Odoo_magento_records_updated_so_far.txt', 'a')


class odooClient:
    def __init__(self):
        self.items = []
        self.vendor = []
    def insert_records(self, items, vandor):
        url = 'https://odoo-dev.brandrange.com'
        db = 'BrandRange'
        username = 'scrapper@oc.com'
        password = '123#'
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        '''for odoo'''
        # if len(models.execute_kw(db, uid, password, 'res.partner', 'search_read',[[['name', '=', vandor]]],{'fields': ['name']}))!=0:
        #     vendor_id = models.execute_kw(db, uid, password, 'res.partner', 'search_read', [[['name', '=', vandor]]], {'fields': ['name']})[0]['id']
        # else:
        #     vendor_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{'name': vandor,}])
        # vendor_id = 1364
        # headersMagentoPriceUpdate = {'accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
        for item in items:
            # originalPrice = item['original_price']
            # del (item['original_price'])
            # item['partner_id'] = vandor
            # try:
            #     if item['group_sku'] == models.execute_kw(db, uid, password, 'product.template', 'search_read', [[['product_code', '=', item['group_sku']]]])[0]['product_code']:
            #         id = models.execute_kw(db, uid, password, 'product.product', 'search_read', [[['default_code', '=', item['product_sku']]]])[0]['id']
            #         try:
            #             # payload_us = {
            #             #     "prices": [
            #             #         {
            #             #             "price": originalPrice,
            #             #             "store_id": 5,
            #             #             "sku": item['product_sku'],
            #             #         }
            #             #     ]
            #             # }
            #             # resp = requests.post('https://admin.brandrange.com/index.php/rest/V1/products/base-prices', headers=headersMagentoPriceUpdate, data=json.dumps(payload_us))
            #             price = models.execute_kw(db, uid, password, 'magento.price.list', 'create', [{'source': 'website', 'website_ids': [3], 'original_price': originalPrice, 'reference': item['ref'], 'partner_id': item['partner_id'], 'rrp': originalPrice, 'group_sku': item['group_sku'], 'product_sku': item['product_sku']}])
            #             logger.info(f'data Sent to Magento for USD')
            #             outputlogfile.write('USD Price: ' + item['product_sku'] + ' ' + str(originalPrice) + '\n')
            #             outputlogfile.flush()
            #             if 'AED' in item['serial_no']:
            #                 website_ids = [1]
            #                 try:
            #                     existing_price = models.execute_kw(db, uid, password, 'product.pricelist.item', 'search_read', [[['product_id', '=', id], ['pricelist_id', '=', 1]]])[0]['fixed_price']
            #                 except:
            #                     existing_price = 0
            #                 # payload_en = {
            #                 #     "prices": [
            #                 #         {
            #                 #             "price": item['retail_price'],
            #                 #             "store_id": 1,
            #                 #             "sku": item['product_sku'],
            #                 #         }
            #                 #     ]
            #                 # }
            #                 # payload_ar = {
            #                 #     "prices": [
            #                 #         {
            #                 #             "price": item['retail_price'],
            #                 #             "store_id": 2,
            #                 #             "sku": item['product_sku'],
            #                 #         }
            #                 #     ]
            #                 # }
            #                 if item['retail_price'] != existing_price:
            #                     # resp = requests.post('https://admin.brandrange.com/index.php/rest/V1/products/base-prices', headers=headersMagentoPriceUpdate, data=json.dumps(payload_en))
            #                     # resp = requests.post('https://admin.brandrange.com/index.php/rest/V1/products/base-prices', headers=headersMagentoPriceUpdate, data=json.dumps(payload_ar))
            #                     price = models.execute_kw(db, uid, password, 'magento.price.list', 'create', [{'source': 'website', 'website_ids': website_ids, 'original_price': originalPrice, 'reference': item['ref'], 'partner_id': item['partner_id'], 'rrp': item['retail_price'], 'group_sku': item['group_sku'], 'product_sku': item['product_sku']}])
            #                     logger.info(f'data Sent to Magento for AED')
            #                     outputlogfile.write('AED Price: ' + item['product_sku'] + ' ' + str(originalPrice) + ' ' + str(item['retail_price']) + '\n')
            #                     outputlogfile.flush()
            #             elif 'KSA' in item['serial_no']:
            #                 website_ids = [2]
            #                 try:
            #                     existing_price = models.execute_kw(db, uid, password, 'product.pricelist.item', 'search_read', [[['product_id', '=', id], ['pricelist_id', '=', 71]]])[0]['fixed_price']
            #                 except:
            #                     existing_price = 0
            #                 # payload_en = {
            #                 #     "prices": [
            #                 #         {
            #                 #             "price": item['retail_price'],
            #                 #             "store_id": 3,
            #                 #             "sku": item['product_sku'],
            #                 #         }
            #                 #     ]
            #                 # }
            #                 # payload_ar = {
            #                 #     "prices": [
            #                 #         {
            #                 #             "price": item['retail_price'],
            #                 #             "store_id": 4,
            #                 #             "sku": item['product_sku'],
            #                 #         }
            #                 #     ]
            #                 # }
            #                 if item['retail_price'] != existing_price:
            #                     # resp = requests.post('https://admin.brandrange.com/index.php/rest/V1/products/base-prices', headers=headersMagentoPriceUpdate, data=json.dumps(payload_en))
            #                     # resp = requests.post('https://admin.brandrange.com/index.php/rest/V1/products/base-prices', headers=headersMagentoPriceUpdate, data=json.dumps(payload_ar))
            #                     price = models.execute_kw(db, uid, password, 'magento.price.list', 'create', [{'source': 'website', 'website_ids': website_ids, 'original_price': originalPrice, 'reference': item['ref'], 'partner_id': item['partner_id'], 'rrp': item['retail_price'], 'group_sku': item['group_sku'], 'product_sku': item['product_sku']}])
            #                     logger.info(f'data Sent to Magento for KSA')
            #                     outputlogfile.write('KSA Price: ' + item['product_sku'] + ' ' + str(originalPrice) + ' ' + str(item['retail_price']) + '\n')
            #                     outputlogfile.flush()
            #
            #
            #         except:
            #             price = models.execute_kw(db, uid, password, 'magento.price.list', 'create', [{'source': 'website', 'website_ids': website_ids, 'original_price': originalPrice, 'reference': item['ref'], 'partner_id': item['partner_id'], 'rrp': item['retail_price'], 'group_sku': item['group_sku'], 'product_sku': item['product_sku']}])
            #             logger.info(f'price Updated to Odoo')
            # except:
            #     try:
            #         if item['group_sku'] == models.execute_kw(db, uid, password, 'product.template', 'search_read', [[['product_code', '=', item['group_sku']]]])[0]['product_code']:
            #             id = models.execute_kw(db, uid, password, 'product.product', 'search_read', [[['default_code', '=', (item['group_sku'] + '-' + item['size']).replace(' ', '-')]]])[0]['id']
            #             try:
            #                 # payload_us = {
            #                 #     "prices": [
            #                 #         {
            #                 #             "price": originalPrice,
            #                 #             "store_id": 5,
            #                 #             "sku": (item['group_sku'] + '-' + item['color'] + '-' + item['size']).replace(' ', '-'),
            #                 #         }
            #                 #     ]
            #                 # }
            #
            #                 # resp = requests.post('https://admin.brandrange.com/index.php/rest/V1/products/base-prices', headers=headersMagentoPriceUpdate, data=json.dumps(payload_us))
            #                 price = models.execute_kw(db, uid, password, 'magento.price.list', 'create', [{'source': 'website', 'website_ids': [3], 'original_price': originalPrice, 'reference': item['ref'], 'partner_id': item['partner_id'], 'rrp': originalPrice, 'group_sku': item['group_sku'], 'product_sku': item['product_sku']}])
            #                 logger.info(f'data Sent to Magento for USD')
            #                 outputlogfile.write('USD Price: ' + item['product_sku'] + ' ' + str(originalPrice) + '\n')
            #                 outputlogfile.flush()
            #                 if 'AED' in item['serial_no']:
            #                     website_ids = [1]
            #                     try:
            #                         existing_price = models.execute_kw(db, uid, password, 'product.pricelist.item', 'search_read', [[['product_id', '=', id], ['pricelist_id', '=', 1]]])[0]['fixed_price']
            #                     except:
            #                         existing_price = 0
            #                     # payload_en = {
            #                     #     "prices": [
            #                     #         {
            #                     #             "price": item['retail_price'],
            #                     #             "store_id": 1,
            #                     #             "sku": (item['group_sku'] + '-' + item['color'] + '-' + item['size']).replace(' ', '-'),
            #                     #         }
            #                     #     ]
            #                     # }
            #                     # payload_ar = {
            #                     #     "prices": [
            #                     #         {
            #                     #             "price": item['retail_price'],
            #                     #             "store_id": 2,
            #                     #             "sku": (item['group_sku'] + '-' + item['color'] + '-' + item['size']).replace(' ', '-'),
            #                     #         }
            #                     #     ]
            #                     # }
            #
            #                     if item['retail_price'] != existing_price:
            #                         # resp = requests.post('https://admin.brandrange.com/index.php/rest/V1/products/base-prices', headers=headersMagentoPriceUpdate, data=json.dumps(payload_en))
            #                         # resp = requests.post('https://admin.brandrange.com/index.php/rest/V1/products/base-prices', headers=headersMagentoPriceUpdate, data=json.dumps(payload_ar))
            #                         price = models.execute_kw(db, uid, password, 'magento.price.list', 'create', [{'source': 'website', 'website_ids': website_ids, 'original_price': originalPrice, 'reference': item['ref'], 'partner_id': item['partner_id'], 'rrp': item['retail_price'], 'group_sku': item['group_sku'], 'product_sku': item['product_sku']}])
            #                         logger.info(f'data Sent to Magento for AED')
            #                         outputlogfile.write('AED Price: ' + item['product_sku'] + ' ' + str(originalPrice) + ' ' + str(item['retail_price']) + '\n')
            #                         outputlogfile.flush()
            #                 elif 'KSA' in item['serial_no']:
            #                     website_ids = [2]
            #                     try:
            #                         existing_price = models.execute_kw(db, uid, password, 'product.pricelist.item', 'search_read', [[['product_id', '=', id], ['pricelist_id', '=', 71]]])[0]['fixed_price']
            #                     except:
            #                         existing_price = 0
            #                     # payload_en = {
            #                     #     "prices": [
            #                     #         {
            #                     #             "price": item['retail_price'],
            #                     #             "store_id": 3,
            #                     #             "sku": (item['group_sku'] + '-' + item['color'] + '-' + item['size']).replace(' ', '-'),
            #                     #         }
            #                     #     ]
            #                     # }
            #                     # payload_ar = {
            #                     #     "prices": [
            #                     #         {
            #                     #             "price": item['retail_price'],
            #                     #             "store_id": 4,
            #                     #             "sku": (item['group_sku'] + '-' + item['color'] + '-' + item['size']).replace(' ', '-'),
            #                     #         }
            #                     #     ]
            #                     # }
            #
            #                     if item['retail_price'] != existing_price:
            #                         # resp = requests.post('https://admin.brandrange.com/index.php/rest/V1/products/base-prices', headers=headersMagentoPriceUpdate, data=json.dumps(payload_en))
            #                         # resp = requests.post('https://admin.brandrange.com/index.php/rest/V1/products/base-prices', headers=headersMagentoPriceUpdate, data=json.dumps(payload_ar))
            #                         price = models.execute_kw(db, uid, password, 'magento.price.list', 'create', [{'source': 'website', 'website_ids': website_ids, 'original_price': originalPrice, 'reference': item['ref'], 'partner_id': item['partner_id'], 'rrp': item['retail_price'], 'group_sku': item['group_sku'], 'product_sku': item['product_sku']}])
            #                         logger.info(f'data Sent to Magento for KSA')
            #                         outputlogfile.write('KSA Price: ' + item['product_sku'] + ' ' + str(originalPrice) + ' ' + str(item['retail_price']) + '\n')
            #                         outputlogfile.flush()
            #
            #             except:
            #                 price = models.execute_kw(db, uid, password, 'magento.price.list', 'create', [{'source': 'website', 'website_ids': website_ids, 'original_price': originalPrice, 'reference': item['ref'], 'partner_id': item['partner_id'], 'rrp': item['retail_price'], 'group_sku': item['group_sku'], 'product_sku': item['product_sku']}])
            #                 logger.info(f'price Updated to Odoo Model:magento.price.list')
            #     except:
            # if 'AED' not in item['serial_no']:
            #     continue
            if len(models.execute_kw(db, uid, password, 'website.scrapper.product', 'search_read',[[['product_sku','=',item['product_sku']]]]))==0:
                id = models.execute_kw(db, uid, password, 'website.scrapper.product', 'create', [item])
                # price = models.execute_kw(db, uid, password, 'magento.price.list', 'create', [{'website_ids':website_ids,'original_price':originalPrice,'reference':id,'partner_id': item['partner_id'], 'rrp': item['retail_price'], 'group_sku': item['group_sku'], 'product_sku': item['product_sku']}])
                logger.info(f'data Sent to Odoo')
            else:
                logger.info(f'data already exists Odoo Model:scrapper.product')
        # try:
        #     return resp.status_code
        # except:
        #     return 200
