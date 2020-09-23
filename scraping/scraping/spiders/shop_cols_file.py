try:
    from pkg_resources import get_distribution
    import pkg_resources.py2_warn
except ImportError:
    pass

import csv
import time
from selenium.webdriver.ie.options import Options
from selenium import webdriver
import scrapy
cols = ['handleId', 'fieldType', 'name', 'description', 'productImageUrl', 'collection', 'sku', 'ribbon', 'price',
        'surcharge', 'visible', 'discountMode', 'discountValue', 'inventory', 'weight', 'productOptionName1',
        'productOptionType1', 'productOptionDescription1', 'productOptionName2', 'productOptionType2',
        'productOptionDescription2', 'productOptionName3', 'productOptionType3', 'productOptionDescription3',
        'productOptionName4', 'productOptionType4', 'productOptionDescription4', 'productOptionName5',
        'productOptionType5', 'productOptionDescription5', 'productOptionName6', 'productOptionType6',
        'productOptionDescription6', 'additionalInfoTitle1', 'additionalInfoDescription1', 'additionalInfoTitle2',
        'additionalInfoDescription2', 'additionalInfoTitle3', 'additionalInfoDescription3', 'additionalInfoTitle4',
        'additionalInfoDescription4', 'additionalInfoTitle5', 'additionalInfoDescription5', 'additionalInfoTitle6',
        'additionalInfoDescription6', 'customTextField1', 'customTextCharLimit1', 'customTextMandatory1',
        'customTextField2', 'customTextCharLimit2', 'customTextMandatory2']
file_ = open('excel_file.csv', 'w', newline='', encoding="utf-8")
writer = csv.DictWriter(file_, fieldnames=cols)
writer.writeheader()
# file_product_links = open('links.txt', 'w')
counter = 0


def get_request(driver, link, sleep=2):
    global counter
    counter += 1
    print('counter : {}'.format(counter))
    if counter >= 7:
        counter = 0
        driver.quit()
        driver = webdriver.Ie()
        driver.set_page_load_timeout(15)
        driver.maximize_window()
        driver.minimize_window()
    try:
        driver.get(link)
        time.sleep(sleep)

    except Exception as e:
        print(str(e))
        time.sleep(2)
        driver = webdriver.Ie()
        driver.set_page_load_timeout(15)
        driver.maximize_window()
        driver.minimize_window()
        get_request(driver, link, sleep=10)

    return driver, scrapy.Selector(text=driver.page_source)


def start_scrape():
    driver = webdriver.Ie()
    driver.set_page_load_timeout(15)
    driver.maximize_window()
    driver.minimize_window()
    driver, response = get_request(driver, "https://shop.coles.com.au/a/brighton-bay-st/everything/browse", 10)
    links = response.css('.cat-nav-item a')
    for link in links:
        main_category = link.css('.item-title ::text').extract_first('')
        link = link.css('::attr(href)').extract_first('')
        link = 'https://shop.coles.com.au{}'.format(link)
        print("main_cat : {}".format(link))
        driver, response_main_cat = get_request(driver, link)
        sub_links = response_main_cat.css('.cat-nav-item a')
        for sub_link in sub_links:
            if sub_link.css('::attr(href)').extract_first('') == '#':
                continue
            sub_category = sub_link.css('.item-title ::text').extract_first('')
            sub_link = sub_link.css('::attr(href)').extract_first('')
            sub_link = 'https://shop.coles.com.au{}'.format(sub_link)
            print("sub_cat : {}".format(sub_link))
            driver, response_sub_cat = get_request(driver, sub_link)
            product_links = response_sub_cat.css('.product-title a ::attr(href)').extract()
            total_pages = 1
            try:
                total_pages = int(response_sub_cat.css('.number ::text').extract()[-1])
            except:
                print('except')
                pass
            print(total_pages)
            for page_number in range(2, total_pages + 1):
                page_link = '{}{}'.format(sub_link[:-1], page_number)
                print("page_cat : {}".format(page_link))
                driver, response_page = get_request(driver, page_link)
                product_links.extend(response_page.css('.product-title a ::attr(href)').extract())
            for product_link in product_links:
                print("product : {}".format(product_link))
                # file_product_links.write(
                #     'https://shop.coles.com.au{} {}:%{}\n'.format(product_link, main_category, sub_category))
                # file_product_links.flush()
                # continue
                product_link = 'https://shop.coles.com.au{}'.format(product_link)
                driver, prod_response = get_request(driver, product_link, 1)
                item = dict()
                item['collection'] = '{};{}'.format(main_category, sub_category)
                # prod_response = scrapy.Selector(text=driver.page_source)
                item['fieldType'] = 'Product'
                item['productImageUrl'] = 'https://shop.coles.com.au{}'.format(prod_response.css('.product-hero-image-container img ::attr(src)').extract_first('')) if prod_response.css('.product-hero-image-container img ::attr(src)').extract_first('') else ''
                item['name'] = ' '.join(prod_response.css('.product .product-title span[aria-hidden="true"]::Text').extract())
                item['price'] = ''.join([v for v in prod_response.css('.price-container ::Text').extract() if v.strip()])
                item['description'] = '\n'.join([v.strip() for v in prod_response.css('.product-specifics.pdp-right-col ::Text').extract() if v.strip()]).replace(',', '')
                writer.writerow(item)
                file_.flush()
    driver.quit()


if __name__ == '__main__':
    counter = 1
    start_scrape()
