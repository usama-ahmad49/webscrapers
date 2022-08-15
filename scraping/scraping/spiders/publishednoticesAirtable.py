import requests
import scrapy
from scrapy.crawler import CrawlerProcess
from seleniumwire import webdriver

import AirtableApi

basekey = 'appCpRqZ4zT3J3PKA'
apikey = 'keyFHOlT21VKJdBVi'
BASE_URL = 'https://api.airtable.com/v0'

table_name = 'publishednotices'

airtable_client = AirtableApi.AirtableClient(apikey, basekey)

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'content-length': '26379',
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': 'ASP.NET_SessionId=1nd3jkpazwuarzird0zu1fts; __utmc=29990078; __utmz=29990078.1624863009.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=29990078.1712190758.1624863009.1624873351.1624889240.3; __utmt=1; AWSALB=C3rnKaTP5dIupkh9Rbl7XxRpBKhpuTx8ftR/233MhEmldoCcsszO+u2sLdNDzgg+C4bRNxS8WWB2Ynxjh1I/0S17e4T6pLjffLZDVSGG43Z5l3xGwgRPBkKYnVfn; __atuvc=7%7C26; __atuvs=60d9d797972d432e003; __utmb=29990078.4.10.1624889240',
    'dnt': '1',
    'origin': 'https://publishednotices.asic.gov.au',
    'referer': 'https://publishednotices.asic.gov.au/browsesearch-notices',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
}

Links = []
Processed = []


class publishednoticesAirtable(scrapy.Spider):
    name = 'publishednotices'

    def start_requests(self):
        url = 'https://publishednotices.asic.gov.au/browsesearch-notices'
        driver = webdriver.Firefox()
        driver.get(url)
        driver.find_element_by_css_selector('#ContentPlaceHolderDefault_INWMasterContentPlaceHolder_INWPageContentPlaceHolder_ucNoticeResult_lvNoticeList > tbody > tr.NoticeTablePager > td > table > tbody > tr > td:nth-child(7) > a').click()
        res = scrapy.Selector(text=driver.page_source)
        driver.quit()
        lastpage = int(res.css('.NoticeTablePager table td')[-1].css('::text').extract_first())
        i = 1
        while i <= lastpage:
            formdata = {
                '__EVENTTARGET': "ctl00$ctl00$ctl00$ctl00$ContentPlaceHolderDefault$INWMasterContentPlaceHolder$INWPageContentPlaceHolder$ucNoticeResult$lvNoticeList",
                '__EVENTARGUMENT': f"Page${i}",
                '__VIEWSTATE': "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",
                'ctl00$ctl00$ctl00$ctl00$ContentPlaceHolderDefault$INWMasterContentPlaceHolder$INWPageContentPlaceHolder$SearchNoticeList_3$txtCompanyNameOrACN': '',
                'ctl00$ctl00$ctl00$ctl00$ContentPlaceHolderDefault$INWMasterContentPlaceHolder$INWPageContentPlaceHolder$SearchNoticeList_3$appoint_hidden': '0',
                'ctl00$ctl00$ctl00$ctl00$ContentPlaceHolderDefault$INWMasterContentPlaceHolder$INWPageContentPlaceHolder$SearchNoticeList_3$notice_hidden': '0',
                'ctl00$ctl00$ctl00$ctl00$ContentPlaceHolderDefault$INWMasterContentPlaceHolder$INWPageContentPlaceHolder$SearchNoticeList_3$ddlNoticeStateList': 'All',
                'ctl00$ctl00$ctl00$ctl00$ContentPlaceHolderDefault$INWMasterContentPlaceHolder$INWPageContentPlaceHolder$SearchNoticeList_3$state_hidden': '0',
                'ctl00$ctl00$ctl00$ctl00$ContentPlaceHolderDefault$INWMasterContentPlaceHolder$INWPageContentPlaceHolder$SearchNoticeList_3$chkExcludeDeregistrationNotices': 'on',
                'ctl00$ctl00$ctl00$ctl00$ContentPlaceHolderDefault$INWMasterContentPlaceHolder$INWPageContentPlaceHolder$SearchNoticeList_3$txtAppointeeSolicitorName': '',
                'ctl00$ctl00$ctl00$ctl00$ContentPlaceHolderDefault$INWMasterContentPlaceHolder$INWPageContentPlaceHolder$SearchNoticeList_3$ddlDateType': '0',
                'ctl00$ctl00$ctl00$ctl00$ContentPlaceHolderDefault$INWMasterContentPlaceHolder$INWPageContentPlaceHolder$SearchNoticeList_3$txtDateTypeFrom': '',
                'ctl00$ctl00$ctl00$ctl00$ContentPlaceHolderDefault$INWMasterContentPlaceHolder$INWPageContentPlaceHolder$SearchNoticeList_3$txtDateTypeTo': '',
                '__VIEWSTATEGENERATOR': 'CA0B0334',
                '__VIEWSTATEENCRYPTED': ''
            }
            i += 1
            req = requests.post(url='https://publishednotices.asic.gov.au/browsesearch-notices', data=formdata, headers=headers)
            res = scrapy.Selector(text=req.content.decode('utf-8'))
            for link in res.css('.NoticeTable .button.plain.addurlparam::attr(href)').extract():
                Links.append(f'https://publishednotices.asic.gov.au{link}')
        for url in Links:
            yield scrapy.Request(url=url)

    def parse(self, response, **kwargs):
        item = dict()
        item['url'] = response.url
        if 'Company ' in response.css('.boxinnerbody .boxinnersub')[0].css('::text').extract_first():
            companyName =''
            ACN =''
            for res in response.css('.boxinnerbody .boxinnercontent')[0].css('.tbl tr'):
                if 'Company:' in res.css('.col1::text').extract_first():
                    companyName +=res.css('.col2::text').extract_first()+' || '
                if 'ACN:' in res.css('.col1::text').extract_first():
                    ACN += res.css('.col2::text').extract_first()+' || '
            try:
                item['CompanyName'] = companyName
            except:
                pass
            try:
                item['CompanyNumber'] = ACN
            except:
                pass

            try:
                item['Status'] = response.css('.boxinnerbody .boxinnercontent')[0].css('.tbl')[-1].css('.col2 ::text').extract_first()
            except:
                pass
            try:
                item['Appointment Date'] = response.css('.boxinnerbody .boxinnercontent')[0].css('.tbl')[-1].css('.col2 ::text').extract()[1]
            except:
                pass

        try:
            item['Notice'] = response.css('.shadow h2::text').extract_first()
        except:
            pass

        if 'Resolution' in response.css('.boxinnerbody .boxinnersub')[1].css('::text').extract_first():
            try:
                item['Liquidators'] = response.css('.boxinnerbody .boxinnercontent')[2].css('p::text').extract_first()
            except:
                pass
            try:
                item['DateCreated']=response.css('.boxinnerbody .boxinnercontent')[2].css('.tbl td.col2::text').extract_first().strip()
            except:
                pass
        if 'Appointment details' in response.css('.boxinnerbody .boxinnersub')[1].css('::text').extract_first():
            try:
                item['Administrator'] = response.css('.boxinnerbody .boxinnercontent')[1].css('.tbl .col2::text').extract_first()
            except:
                pass
        if 'proof of debt' in response.css('.boxinnerbody .boxinnersub')[1].css('::text').extract_first():
            try:
                item['Liquidators'] = response.css('.boxinnerbody .boxinnercontent')[2].css('p::text').extract_first()
            except:
                pass
            try:
                item['DateCreated']=response.css('.boxinnerbody .boxinnercontent')[2].css('.tbl td.col2::text').extract_first().strip()
            except:
                pass

        Processed.append(item)

    def close(spider, reason):
        airtable_client.insert_records(table_name, Processed)


process = CrawlerProcess({
    'USER_AGENT': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36"})

process.crawl(publishednoticesAirtable)
process.start()