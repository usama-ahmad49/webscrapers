import json
import logging
import xmlrpc.client
import requests
import time
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



def getsku():
    url = 'https://odoo.brandrange.com'
    db = 'BrandRange'
    username = 'scrapper@oc.com'
    password = 'scrapper123#*'
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    # sku = models.execute_kw(db, uid, password, 'product.template', 'search_read', [[['product_code', '=', '6595683319921-Black-OS']]])[0]['product_code']
    sss = models.execute_kw(db, uid, password, 'product.template', 'fields_get',[],{})
if __name__ == '__main__':
    getsku()
