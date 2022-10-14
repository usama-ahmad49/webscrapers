from scrapy.crawler import CrawlerProcess
import scrapy
import requests
import common
import json
cookies = {
    'JSESSIONID': 'A078994E973B3BCD800655C5EA08689E',
    '_gcl_au': '1.1.1621299775.1664983814',
    '_ga': 'GA1.3.518487548.1664983819',
    '_gid': 'GA1.3.601428599.1664983819',
    '_gat': '1',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # Requests sorts cookies= alphabetically
    # 'Cookie': 'JSESSIONID=A078994E973B3BCD800655C5EA08689E; _gcl_au=1.1.1621299775.1664983814; _ga=GA1.3.518487548.1664983819; _gid=GA1.3.601428599.1664983819; _gat=1',
    'DNT': '1',
    'Pragma': 'no-cache',
    'Referer': 'https://physio.org.nz/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

params = {
    'Action': 'List Physios',
}


class physio(scrapy.Spider):
    name = 'physio'
    STAT_FILE = 'physio.stat'
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
    }
    crawled = []
    def start_requests(self):
        self.crawled = common.load_crawled(self.STAT_FILE)

        resp = requests.get('https://physio.org.nz/Company', params=params, cookies=cookies, headers=headers)
        JDATA = json.loads(resp.text)

        for data in JDATA['Branches']:
            url = f'https://physio.org.nz/CompanyProfile?Action=View&CompanyProfile_id={data["ID"]}'
            if url not in self.crawled:
                self.crawled.add(url)
                yield scrapy.Request(url=url, meta={'data':data})

    def parse(self, response, **kwargs):
        data = response.meta['data']
        item = dict()
        item['url'] = response.url
        item['name'] = data['Name']
        item['reg_no'] = data['ID']
        item['location'] = data['DisplayAddress']
        item['area_of_interest'] = ', '.join(data['Tags'])
        item['phone_number'] = response.css('ul.company-contact-details:nth-child(1) li:nth-child(1) > a::text').extract_first(
            '').strip()
        item['website'] = response.css(
            'ul.company-contact-details:nth-child(1)  li:nth-child(2) > a::text').extract_first('').strip()

        profile = common.Profile(
            name=item['name'], profession='Physiotherapist',
            location=item.get('location'), reg_no=item['reg_no'],
            url=item['url'], phone_number=item.get('phone_number'),
            website=item.get('website'),area_of_interest = item['area_of_interest']
        )
        common.to_thunderstorm([profile], 'physio')

    def close(spider, reason):
        """
        This function saves all the scrapped URLs in the stat file to keep log for further scraping
        """
        common.update_crawled(spider.crawled, spider.STAT_FILE)




if __name__ == '__main__':
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(physio)
    process.start()