import json
import time
import scrapy
from scrapy.crawler import CrawlerProcess
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from seleniumwire import webdriver

# headers1 = {
#     "accept": "application/json",
#     "accept-language": "en-US,en;q=0.9",
#     "cache-control": "no-cache",
#     "content-type": "application/json",
#     "dnt": "1",
#     "origin": "https://www.pinnacle.bet",
#     "pragma": "no-cache",
#     "referer": "https://www.pinnacle.bet/",
#     "sec-fetch-dest": "empty",
#     "sec-fetch-mode": "cors",
#     "sec-fetch-site": "cross-site",
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
#     "x-api-key": "CmX2KcMrXuFmNg6YFbmTxE0y9CIrOi0R",
#     "x-device-uuid": "37507033-467a2b28-efc18411-a7ba7108"
# }

headers2 = {
"accept": "application/json",
"accept-language": "en-US,en;q=0.9",
"cache-control": "no-cache",
"content-type": "application/json",
"dnt": "1",
"origin": "https://www.pinnacle.bet",
"pragma": "no-cache",
"referer": "https://www.pinnacle.bet/",
"sec-fetch-dest": "empty",
"sec-fetch-mode": "cors",
"sec-fetch-site": "cross-site",
"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
"x-api-key": "CmX2KcMrXuFmNg6YFbmTxE0y9CIrOi0R",
"x-device-uuid": "37507033-467a2b28-efc18411-a7ba7108",
}

fileinput = open('pinnaclebetinput.txt', 'r')
inputurl = fileinput.read().split('\n')


# class pinnaclebet(scrapy.Spider):
#     name = 'pinnaclebet'
#
#     def start_requests(self):
#         json_urls = []
#         driver = webdriver.Firefox()
#         for url in inputurl:
#             driver.get(url=url)
#             time.sleep(40)
#             # WebDriverWait(driver, 120).until(expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[2]/main/div/div/div[3]')))
#             json_urls.append([v for v in driver.requests if 'https://guest.api.arcadia.pinnacle.com/0.1/leagues' in v.path and '/matchups' in v.path][0].path)
#         driver.quit()
#         for json_url in json_urls:
#             yield scrapy.Request(url=json_url, headers=headers1, method='GET')
#
#     def parse(self, response):
#         json_data = json.loads(response.text)
#         for code in json_data:
#             id = code.get('id')
#             fname=code.get('parent').get('participants')[0].get('name').replace(' ','-')
#             lname=code.get('parent').get('participants')[1].get('name').replace(' ','-')
#             league=(code.get('league').get('name').replace(' - ','-')).replace(' ','-')
#             sport=code.get('league').get('sport').get('name')
#             url='https://www.pinnacle.bet/en/{}/{}/{}-vs-{}/{}/'.format(sport,league,fname,lname,id)
#             driver = webdriver.Firefox()
#             driver.get(url=url)
#             time.sleep(40)
#             json_url=[v for v in driver.requests if 'https://guest.api.arcadia.pinnacle.com/0.1/matchups/' in v.path][0].path
#             yield scrapy.Request(url=json_url, headers=headers2, callback=self.parse_data)
#     def parse_data(self, response):
#         pass
#
#
# process = CrawlerProcess({
#     'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
# })
#
# process.crawl(pinnaclebet)
# process.start()


def getdata():
    driver=webdriver.Firefox()
    url_match=[]
    for url in inputurl:
        driver.get(url)
        time.sleep(35)
        ps = scrapy.Selector(text=driver.page_source)
        driver.quit()
        for resp in ps.css('.style_container__3D79z'):
            url_match.append('https://www.pinnacle.bet'+resp.css('::attr(href)').extract_first())
        for url in url_match:
            driver=webdriver.Firefox()
            driver.get(url=url)
            time.sleep(35)
            driver.find_element_by_class_name('style_flexButton__3lKmg').click()
            for seemore in driver.find_elements_by_css_selector('div.style_marketGroup__1LRLw > div > div > div > span > i'):
                seemore.click()
            ps = scrapy.Selector(text=driver.page_source)
            titles=[v for v in ps.css('.style_title__2Y8r7.collapse-title span::text').extract()[:4] if 'See more' not in v and 'See less' not in v]
            match_teams=' vs '.join(ps.css('.style_participants__3SkHT ::text').extract()[1:])
            titles_0 =ps.css('.style_container__1MuSF.style_gutters__3uqPU.style_col3__yCJzD a span::text').extract()[0]
            titles_1 = ps.css('.style_container__1MuSF.style_gutters__3uqPU.style_col3__yCJzD a span::text').extract()[2]
            titles_2 = ps.css('.style_container__1MuSF.style_gutters__3uqPU.style_col3__yCJzD a span::text').extract()[4]
            moneyline_results=[v for v in ps.css('.style_container__1MuSF.style_gutters__3uqPU.style_col3__yCJzD a span::text').extract() if '.' in v]
            handicap_results_team1=''




if __name__ == '__main__':
    getdata()
