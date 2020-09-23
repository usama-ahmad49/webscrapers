import time

from selenium import webdriver

try:
    import pkg_resources.py2_warn
except ImportError:
    pass

import csv
import datetime

import scrapy
from scrapy.crawler import CrawlerProcess

Email='famfabrix@gmail.com'
account='FAM004'
pin='1653'

csv_columns = ["Item_ID", "Item_Code", "Item_Type", "Brand_Name", "Item_Name", "Item_Published", "Item_Is_featured",
               "Item_Visibility", "Item_Discription_small", "Item_Discription_full", "Item_Color", "Avalible_Sizes",
               "Item_Date_sale", "Item_Date_Ends", "Item_Tax_Status", "Item_Tax_Class", "Item_InStock?", "Item_Stock",
               "Item_Low_Stock", "Item_Backorders_Allowed", "Item_Sold_individually?", "Item_Allow_Customer_Review",
               "Item_Purchase", "Item_Sales_Price", "Item_Regular_Price", "Item_Catagories", "Item_Tags",
               "Item_Shipping_Class", "ImageUrl", "Item_Download_Limit", "Item_Download_Expiry_date", "Item_Parent",
               "Item_Grouped_Products", "Item_Upsells", "Item_Cross-sells", "Item_External_Url", "Item_Button_Text",
               "Item_position", "Item_Attribute1_name", "Item_Attribute1_value", "Item_Attribute1_visible",
               "Item_Attribute1_global", "Item_Attribute2_name", "Item_Attribute2_value", "Item_Attribute2_visible",
               "Item_Attribute2_global", "Item_Attribute1_default", "Item_Attribute2_default", "Item_Sizes",
               "Item_Weight", "Item_Carton_Qty"]
csvfile = open('absoluteapperal-{}.csv'.format(datetime.datetime.now().date()), 'w', newline='', encoding="utf-8")
writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
writer.writeheader()


class AbsoluteApparel(scrapy.Spider):
    name = 'absoluteapparel'
    # start_urls = ['https://absoluteapparel.co.uk/']
    def start_requests(self):
        self.driver = webdriver.Firefox()
        self.driver.get('https://absoluteapparel.co.uk/Login')
        username_field = self.driver.find_element_by_name('TemplatePage$BOX_001$MODULE76_4$txtEmailAddress')
        username_field.send_keys(Email)
        password_field = self.driver.find_element_by_name('TemplatePage$BOX_001$MODULE76_4$txtAccountNumber')
        password_field.send_keys(account)
        pin_field = self.driver.find_element_by_name('TemplatePage$BOX_001$MODULE76_4$txtPIN')
        pin_field.send_keys(pin)
        agreement_field = self.driver.find_element_by_name('TemplatePage$BOX_001$MODULE76_4$ckTerms')
        agreement_field.click()
        time.sleep(1)
        submit = self.driver.find_element_by_id('TemplatePage_BOX_001_MODULE76_4_bnLogin')
        submit.click()
        time.sleep(5)
        yield scrapy.Request('https://absoluteapparel.co.uk/')

    def parse(self, response):
        for category_link in response.css('.newnav li a::attr(href)').extract():
            yield scrapy.Request('https://absoluteapparel.co.uk{}'.format(category_link), callback=self.parse_category)

    def parse_category(self, response):
        print('{}: {}'.format(len(response.css('#TemplatePage_BOX_002_MODULE84_4_DataList tr td a ::attr(href)').extract()), response.url))
        for product in response.css('#TemplatePage_BOX_002_MODULE84_4_DataList tr td a ::attr(href)').extract():
            self.driver.get(product)
            yield scrapy.Request(product, callback=self.parse_product, meta={'source': scrapy.Selector(text=self.driver.page_source)})

    def parse_product(self, response):
        response = response.meta['source']
        item = dict()
        item['Item_ID'] = response.url.split("/")[-1]
        item['Item_Code'] = response.css('#TemplatePage_MODULE200_3_ASPxRoundPanel1_lCode ::text').extract()[0]
        item['Item_Type'] = ''
        item['Brand_Name'] = response.css('#TemplatePage_MODULE200_3_ASPxPageControl1_lBrand ::text').extract()[0]
        item['Item_Name'] = response.css('#TemplatePage_MODULE200_3_ASPxRoundPanel1_RPHT ::text').extract()[0]
        item['Item_Published'] = '1'
        item['Item_Is_featured'] = '0'
        item['Item_Visibility'] = 'Visible'
        item['Item_Discription_small'] = ', '.join(
            response.css('#TemplatePage_MODULE200_3_ASPxPageControl1_lMarketing ::text').extract()[2:6]).replace('•',
                                                                                                                 '').encode(
            "ascii", "ignore")
        item['Item_Discription_full'] = ', '.join(
            response.css('#TemplatePage_MODULE200_3_ASPxPageControl1_lMarketing ::text').extract()[1:]).replace('•',
                                                                                                                '').encode(
            "ascii", "ignore")
        item['Item_Color'] = ', '.join([v for v in response.css(
            '#TemplatePage_MODULE200_3_ASPxRoundPanel1_tableColours tr td span ::text').extract() if v.strip()]).encode(
            "ascii", "ignore")
        item['Avalible_Sizes'] = ', '.join(response.css(
            '#TemplatePage_MODULE200_3_ASPxRoundPanel1_tableQuantity tr td span ::text').extract()).encode("ascii",
                                                                                                           "ignore")
        item['Item_Date_sale'] = ''
        item['Item_Date_Ends'] = ''
        item['Item_Tax_Status'] = 'taxable'
        item['Item_Tax_Class'] = ''
        item['Item_InStock?'] = '1'
        item['Item_Stock'] = ''
        item['Item_Low_Stock'] = ''
        item['Item_Backorders_Allowed'] = '0'
        item['Item_Sold_individually?'] = '0'
        item['Item_Allow_Customer_Review'] = '1'
        item['Item_Purchase'] = ''
        item['Item_Sales_Price'] = ''
        item['Item_Regular_Price'] = ''
        item['Item_Catagories'] = ''  # Item catagories are not present on product page
        item['Item_Tags'] = ''
        item['Item_Shipping_Class'] = ''
        item['ImageUrl'] = 'https://absoluteapparel.co.uk{}'.format(
            response.css('#TemplatePage_MODULE200_3_imgProductImage ::attr(src)').extract_first(''))
        item['Item_Download_Limit'] = ''
        item['Item_Download_Expiry_date'] = ''
        item['Item_Parent'] = ''
        item['Item_Grouped_Products'] = ''
        item['Item_Upsells'] = ''
        item['Item_Cross-sells'] = ''
        item['Item_Cross-sells'] = ''
        item['Item_External_Url'] = response.url
        item['Item_Button_Text'] = 'Express Shop'
        item['Item_position'] = ''
        item['Item_Attribute1_name'] = 'number of colours Available'
        item['Item_Attribute1_value'] = [v for v in response.css(
            '#TemplatePage_MODULE200_3_ASPxRoundPanel1_tableColours tr td span ::text').extract() if
                                         v.strip()].__len__()
        item['Item_Attribute1_visible'] = '1'
        item['Item_Attribute1_global'] = '1'
        item['Item_Attribute2_name'] = 'Number of Sizes Available'
        item['Item_Attribute2_value'] = response.css(
            '#TemplatePage_MODULE200_3_ASPxRoundPanel1_tableQuantity tr td span ::text').extract().__len__()
        item['Item_Attribute2_visible'] = '1'
        item['Item_Attribute2_global'] = '1'
        item['Item_Attribute1_default'] = ''
        item['Item_Attribute2_default'] = ''
        yield scrapy.Request('https://absoluteapparel.co.uk/{}'.format(
            response.css('#TemplatePage_MODULE200_3_ASPxRoundPanel1_hypExpert ::attr(href)').extract_first('')),
                             callback=self.parse_product_detail, meta={'item': item})

    def parse_product_detail(self, response):
        item = response.meta['item']
        for detail in response.css('p[align="justify"] ::text').extract():
            if 'Sizes' in detail:
                item['Item_Sizes'] = detail[7:13]
            elif 'Weight' in detail:
                item['Item_Weight'] = detail[8:13]
            elif 'Carton Qty' in detail:
                item['Item_Carton_Qty'] = detail[12:17]
                break
        writer.writerow(item)
        csvfile.flush()
        yield item


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(AbsoluteApparel)
process.start()
