from selenium import webdriver
import time

if __name__ == '__main__':
    urllist = ['http://34.135.192.247/stockx_pricelist_magento_new.csv', 'http://34.135.192.247/stockx_pricelist_magento_new_original.csv',
               'http://34.135.192.247/stockx_pricelist_magento_old.csv', 'http://34.135.192.247/stockx_pricelist_magento_old_original.csv',
               'http://34.135.192.247/stockx_pricelist_odoo_new.csv', 'http://34.135.192.247/stockx_pricelist_odoo_new_original.csv',
               'http://34.135.192.247/stockx_pricelist_odoo_old.csv', 'http://34.135.192.247/stockx_pricelist_odoo_old_original.csv',
               'http://34.135.192.247/cettire_pricelist_magento.csv', 'http://34.135.192.247/cettire_pricelist_magento_original.csv',
               'http://34.135.192.247/cettire_pricelist_odoo.csv', 'http://34.135.192.247/cettire_pricelist_odoo_original.csv',
               ]

    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": r"C:\Users\user\Desktop\StockxFiles"}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chrome_options=options)
    for url in urllist:
        driver.get(url)
        time.sleep(5)
    driver.close()
