import time

import requests
import scrapy
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import json
import csv

csvheaders = ['Title', 'Author','url', 'Category', 'Price', 'MRP', 'Diff Format Prices', 'Rating', 'Image',
              'Product Description',
              'Product Detail', 'Seller Ranking', 'Customer Reviews', 'Short Passage', ]
file = open('E:\Project\genratedfiles\Booksdata.csv', 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(file, csvheaders)
writer.writeheader()

driver = webdriver.Ie()
driver.set_page_load_timeout(15)
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': 'session-id=259-9661643-7739343; i18n-prefs=INR; ubid-acbin=262-1125438-2520542; '
              'session-token=ZWRW+0M2428kJZGKqyOtqSITbQaZ9FHTkSu4udq3p+2aefOx/Yaymjv'
              '/L71W3U1wJIAXeYebF7ziNNqTzOqxlSqLP0UrJXWWsO50wNTQ/E/Yh7w'
              '/I2WT90citXthkjEhwmG9ICS6gXXf0RQPLeBmkYw7ell1yTrt51cGPOzEybfJqchV2CbQt3JzlFFXxT8D; visitCount=5; '
              'csm-hit=tb:MESD84BPSYPYZ3AWM08X+s-5QEQQ2WCADE1H6572W36|1600760458434&t:1600760458434&adb:adblk_no; '
              'session-id-time=2082787201l',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/85.0.4183.102 Safari/537.36',
}


def getBookData(url):
    print(url)
    try:
        driver.get(url=url)
    except TimeoutException:
        try:
            driver.get(url=url)
        except:
            print('Loading failed: ' + url) # yahan error aa rha hai after Message: Failed to navigate to...
            return

    pageSource = driver.page_source
    response = scrapy.Selector(text=pageSource)
    item = dict()
    item['url']=url
    if response.css('#productTitle') and response.css('#productSubtitle'):
        item['Title'] = (response.css('#productTitle ::text').extract_first().strip() + ' ' + response.css(
            '#productSubtitle ::text').extract_first()).replace('\n', '')
    else:
        return
    if response.css('#bylineInfo .a-link-normal.contributorNameID'):
        item['Author'] = response.css('#bylineInfo .a-link-normal.contributorNameID ::text').extract_first()
    elif response.css('#bylineInfo .a-link-normal'):
        item['Author'] = response.css('#bylineInfo .a-link-normal ::text').extract_first()
    else:
        return

    if response.css('#wayfinding-breadcrumbs_feature_div'):
        item['Category'] = ', '.join(response.css(
            '#wayfinding-breadcrumbs_feature_div .a-link-normal.a-color-tertiary ::text').extract()).replace('\n',
                                                                                                             '').strip()
    else:
        item['Category'] = ''
    if response.css('#buyNewSection'):
        item['Price'] = response.css('#buyNewSection span::text').extract_first()
        item['MRP'] = response.css('span[class="a-color-secondary a-text-strike"] ::text').extract_first()
    elif response.css('.a-lineitem.a-spacing-micro'):
        item['Price'] = ''.join(response.css('.kindle-price ::text').extract()[:7]).replace('\n', '')
        item['MRP'] = ''.join(response.css('.print-list-price ::text').extract()).replace('\n', '')
    else:
        return
    if response.css('.a-fixed-left-grid-col.aok-align-center.a-col-right'):
        item['Rating'] = response.css('#reviewsMedley .a-size-medium.a-color-base ::text').extract_first() +' From '+ response.css('#acrCustomerReviewText ::text').extract_first()
    else:
        item['Rating'] = ' '
    if response.css('#imgBlkFront'):
        item['Image'] = response.css('#imgBlkFront ::attr(src)').extract_first()
        if(response.css('#imageBlockThumbs')):
            item['Image']=item['Image']+' , '+(' , '.join(response.css('#imageBlockThumbs img::attr(src)').extract()))
    elif response.css('#ebooksImgBlkFront'):
        item['Image'] = response.css('#ebooksImgBlkFront ::attr(src)').extract_first()
    else:
        return

    if response.css('#twister'):
        price_list = []
        for pr in response.css('#twister .top-level.unselected-row'):
            Diff_Format_Price = dict()
            if pr.css('.a-size-small.a-color-price'):
                Diff_Format_Price['Format'] = pr.css('.a-size-small.a-color-base ::text').extract_first()
                Diff_Format_Price['Price'] = pr.css('.a-size-small.a-color-price ::text').extract_first()
                price_list.append(Diff_Format_Price)

            else:
                Diff_Format_Price['Format'] = pr.css('.a-size-small.a-color-base ::text').extract_first()
                Diff_Format_Price['Price'] = 'Price/Product is Unavalible'
                price_list.append(Diff_Format_Price)

        item['Diff Format Prices'] = json.dumps(price_list)
    else:
        return
    if response.css('#editorialReviews_feature_div'):
        item['Product Description'] = ''.join(response.css(
            '#editorialReviews_feature_div .a-row.a-expander-container.a-expander-extend-container ::text').extract()).replace(
            '\n', '')
    else:
        return
    if response.css('#detailBullets_feature_div #detailBullets_feature_div'):
        productdets = ''.join(response.css('#detailBullets_feature_div #detailBullets_feature_div *::text').extract()).replace('\n',' ').strip().split('   ')
        productdetsDict = dict()
        for productdet in productdets:
            if productdet == '':
                continue
            else:
                keynvalue = productdet.split(':')
                productdetsDict[keynvalue[0]] = keynvalue[1]
        item['Product Detail'] =json.dumps(productdetsDict)
    else:
        item['Product Detail'] = ' '
    if response.xpath('//*[@id="detailBulletsWrapper_feature_div"]/ul[1]//text()'):
        sellerRank=''.join(response.xpath('//*[@id="detailBulletsWrapper_feature_div"]/ul[1]//text()').extract()).replace('\n', '').split('#')
        item['Seller Ranking'] = json.dumps(sellerRank)
    else:
        item['Seller Ranking']=' '
    if response.xpath('//*[@id="detailBullets_averageCustomerReviews"]/span[3]//text()'):
        item['Customer Reviews'] = ''.join(
            response.xpath('//*[@id="detailBullets_averageCustomerReviews"]/span[3]//text()').extract()).replace('\n',
                                                                                                                 '')
    else:
        return
    if driver.find_element_by_id('bookDesc_iframe'):
        iframe = driver.find_element_by_id('bookDesc_iframe')
        driver.switch_to.frame(iframe)
        pgsource = driver.page_source
        resp = scrapy.Selector(text=pgsource)
        item['Short Passage'] = ''.join(resp.css('#iframeContent ::text').extract()).replace('\n', '')
    else:
        return

    writer.writerow(item)
    file.flush()

    return


def getBooksList(url):
    resp = requests.get(url=url)
    respon = resp.text
    response = scrapy.Selector(text=respon)
    Book_Links = []

    for li in response.css('#mainResults .a-link-normal.s-access-detail-page.s-color-twister-title-link.a-text-normal'):
        book_link = li.attrib.get('href')
        Book_Links.append(book_link)
    i = 2
    if (response.css('#pagn .pagnDisabled')):
        totalPages = int(response.css('#pagn .pagnDisabled ::text').extract_first())
    else:
        return
    while i <= 1:  # remove 3 and put totalPages in production
        next_page_url = 'https://www.amazon.in/s?rh=n%3A976389031%2Cn%3A%21976390031%2Cn%3A1318158031&page={}&qid' \
                        '=1600757238&ref=lp_1318158031_pg_{}'.format(i, i)
        print(str(i) + ' page')
        i = i + 1
        try:
            driver.get(url=next_page_url)
        except TimeoutException:
            try:
                driver.get(url=next_page_url)
            except:
                print('Loading failed: ' + next_page_url)
                continue
        time.sleep(2)
        ps = driver.page_source
        response = scrapy.Selector(text=ps)
        for lst in response.css('.s-main-slot.s-result-list.s-search-results.sg-row .a-link-normal.a-text-normal'):
            book_2_link = 'https://www.amazon.in{}'.format(lst.attrib.get('href'))
            Book_Links.append(book_2_link)

    for ind_book_link in Book_Links:
        getBookData(ind_book_link)

    return


def getBooksByGenres():
    url = 'https://www.amazon.in/Books/b/?ie=UTF8&node=976389031&ref_=nav_cs_books'
    links = []
    resp = requests.get(url=url)
    respon = resp.text
    response = scrapy.Selector(text=respon)
    for list in response.css('.a-unordered-list.a-nostyle.a-vertical.s-ref-indent-one .a-link-normal.s-ref-text-link'):
        link = list.attrib.get('href')
        links.append(link)
    for link in links:
        getBooksList(link)
    return


if __name__ == '__main__':
    getBooksByGenres()
    driver.quit()
