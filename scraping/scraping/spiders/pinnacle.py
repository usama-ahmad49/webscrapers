try:
    from pkg_resources import get_distribution
    import pkg_resources.py2_warn
except ImportError:
    pass

import time

import scrapy
from seleniumwire import webdriver
from xlwt import Workbook


# Workbook is created


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


if __name__ == '__main__':
    fileinput = open('pinnaclebetinput.txt', 'r')
    inputurl = fileinput.read().split('\n')
    driver = webdriver.Chrome()
    driver.maximize_window()
    for url in inputurl:
        driver.get(url)
        got = False
        while not got:
            response = scrapy.Selector(text=driver.page_source)
            if response.css('a[data-test-id="Event.MarketCnt"] ::attr(href)').extract():
                got = True
            else:
                time.sleep(1)

        for match_link in response.css('a[data-test-id="Event.MarketCnt"] ::attr(href)').extract():
            link = 'https://www.pinnacle.bet{}'.format(match_link)
            driver.get(link)
            got = False
            inner_response = scrapy.Selector(text=driver.page_source)
            while not inner_response.css('div.style_primary__awRGO.style_marketGroup__1LRLw'):
                time.sleep(1)
                inner_response = scrapy.Selector(text=driver.page_source)
            try:
                driver.find_element_by_xpath('//*[@id="root"]/div/div/div[2]/main/div/div[2]/div[1]/div/button[1]').click()
                time.sleep(1)
                for e in driver.find_elements_by_class_name('style_title__2Y8r7.collapse-title.style_alternateLineCollapseTitle__1w5sl'):
                    e.click()
                    time.sleep(1)
            except:
                pass
            inner_response = scrapy.Selector(text=driver.page_source)
            team1 = None
            team2 = None
            wb = Workbook()
            sheet1 = wb.add_sheet('Sheet 1')
            title = None
            row_start = 8
            for index, div in enumerate(inner_response.css('div.style_primary__awRGO.style_marketGroup__1LRLw')):
                if index == 0:
                    title = ''.join(div.css('.style_titleText__jlbrV.ellipsis ::text').extract())
                    sheet1.write(0, 0, title)
                    sheet1.write(0, 1, div.css('a')[0].css('.label ::Text').extract_first(''))
                    sheet1.write(0, 2, div.css('a')[1].css('.label ::Text').extract_first(''))
                    sheet1.write(0, 3, div.css('a')[2].css('.label ::Text').extract_first(''))
                    sheet1.write(1, 1, div.css('a')[0].css('.price ::Text').extract_first(''))
                    sheet1.write(1, 2, div.css('a')[1].css('.price ::Text').extract_first(''))
                    sheet1.write(1, 3, div.css('a')[2].css('.price ::Text').extract_first(''))
                elif index == 1:
                    title = ''.join(div.css('.style_titleText__jlbrV.ellipsis ::text').extract())
                    sheet1.write(3, 0, title)
                    team1 = div.css('.style_subHeading__1pBR2 li ::Text').extract()[0]
                    team2 = div.css('.style_subHeading__1pBR2 li ::Text').extract()[1]
                    sheet1.write(4, 0, div.css('.style_subHeading__1pBR2 li ::Text').extract()[0])
                    sheet1.write(6, 0, div.css('.style_subHeading__1pBR2 li ::Text').extract()[1])
                    data = div.css('a ::Text').extract()
                    ind = 0
                    col1 = 1
                    col2 = 1
                    row = 4
                    row2 = 6
                    for sub_data in chunks(data, 2):

                        if not ind % 2:
                            sheet1.write(row, col1, sub_data[0])
                            sheet1.write(row + 1, col1, sub_data[1])
                            col1 += 1
                        if ind % 2:
                            sheet1.write(row2, col2, sub_data[0])
                            sheet1.write(row2 + 1, col2, sub_data[1])
                            col2 += 1
                        ind += 1

                else:
                    sheet1.write(row_start, 0, ''.join(div.css('.style_titleText__jlbrV.ellipsis ::text').extract()).replace('See less', ''))
                    try:
                        sheet1.write(row_start + 1, 0, div.css('.style_subHeading__1pBR2 li ::Text').extract()[0])
                        sheet1.write(row_start + 3, 0, div.css('.style_subHeading__1pBR2 li ::Text').extract()[1])
                        data = div.css('a ::Text').extract()
                        if ''.join(div.css('.style_titleText__jlbrV.ellipsis ::text').extract()) == 'Team Total – Match':
                            data = [data[0], data[1], data[4], data[5], data[2], data[3], data[6], data[7]]
                        ind = 0
                        col1 = 1
                        col2 = 1
                        row = row_start + 1
                        row2 = row_start + 3
                        for sub_data in chunks(data, 2):

                            if not ind % 2:
                                sheet1.write(row, col1, sub_data[0])
                                sheet1.write(row + 1, col1, sub_data[1])
                                col1 += 1
                            if ind % 2:
                                sheet1.write(row2, col2, sub_data[0])
                                sheet1.write(row2 + 1, col2, sub_data[1])
                                col2 += 1
                            ind += 1

                    except:
                        for label_index, label in enumerate(div.css('.label ::Text').extract()):
                            sheet1.write(row_start, label_index + 1, label)
                        for price_index, price in enumerate(div.css('.price ::Text').extract()):
                            sheet1.write(row_start + 1, price_index + 1, price)
                    row_start += 6

            wb.save('{} vs {}.xls'.format(team1, team2))
    driver.close()
    exit()
