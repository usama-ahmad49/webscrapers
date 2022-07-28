import csv
import time

import scrapy
from scrapy.crawler import CrawlerProcess
from seleniumwire import webdriver

header = ['Nume firma', 'Cod Unic de Înregistrare', 'Nr. Înmatriculare', 'EUID', 'Data finantarii:', 'Observatii', 'Poziţia în Topul Firmelor 2020', 'Descrierea firmei', 'Referiri in social media', 'Judet', 'Localitate/Sector', 'Adresa', 'Telefon', 'Fax', 'Mobil', 'Email', 'Persoane din conducere', 'Adresa web', 'Cod CAEN', 'Cifra afaceri 2019', 'Profit Net 2019', 'Datorii 2019', 'Active imobilizate 2019', 'Active circulante 2019', 'Capitaluri proprii 2019', 'Angajați (nr. mediu) 2019', 'Cifra afaceri 2018', 'Profit Net 2018', 'Datorii 2018', 'Active imobilizate 2018', 'Active circulante 2018', 'Capitaluri proprii 2018', 'Angajați (nr. mediu) 2018', 'Cifra afaceri 2017', 'Profit Net 2017', 'Datorii 2017', 'Active imobilizate 2017', 'Active circulante 2017', 'Capitaluri proprii 2017', 'Angajați (nr. mediu) 2017', 'Cifra afaceri 2016', 'Profit Net 2016', 'Datorii 2016',
          'Active imobilizate 2016', 'Active circulante 2016', 'Capitaluri proprii 2016', 'Angajați (nr. mediu) 2016', 'Cifra afaceri 2015', 'Profit Net 2015', 'Datorii 2015', 'Active imobilizate 2015', 'Active circulante 2015', 'Capitaluri proprii 2015', 'Angajați (nr. mediu) 2015', 'Cifra afaceri 2014', 'Profit Net 2014', 'Datorii 2014', 'Active imobilizate 2014', 'Active circulante 2014', 'Capitaluri proprii 2014', 'Angajați (nr. mediu) 2014', 'Cifra afaceri 2013', 'Profit Net 2013', 'Datorii 2013', 'Active imobilizate 2013', 'Active circulante 2013', 'Capitaluri proprii 2013', 'Angajați (nr. mediu) 2013', 'Cifra afaceri 2012', 'Profit Net 2012', 'Datorii 2012', 'Active imobilizate 2012', 'Active circulante 2012', 'Capitaluri proprii 2012', 'Angajați (nr. mediu) 2012', 'Cifra afaceri 2011', 'Profit Net 2011', 'Datorii 2011', 'Active imobilizate 2011', 'Active circulante 2011',
          'Capitaluri proprii 2011', 'Angajați (nr. mediu) 2011', 'Cifra afaceri 2010', 'Profit Net 2010', 'Datorii 2010', 'Active imobilizate 2010', 'Active circulante 2010', 'Capitaluri proprii 2010', 'Angajați (nr. mediu) 2010', 'Cifra afaceri 2009', 'Profit Net 2009', 'Datorii 2009', 'Active imobilizate 2009', 'Active circulante 2009', 'Capitaluri proprii 2009', 'Angajați (nr. mediu) 2009', 'Cifra afaceri 2008', 'Profit Net 2008', 'Datorii 2008', 'Active imobilizate 2008', 'Active circulante 2008', 'Capitaluri proprii 2008', 'Angajați (nr. mediu) 2008', 'Cifra afaceri 2007', 'Profit Net 2007', 'Datorii 2007', 'Active imobilizate 2007', 'Active circulante 2007', 'Capitaluri proprii 2007', 'Angajați (nr. mediu) 2007', 'Cifra afaceri 2006', 'Profit Net 2006', 'Datorii 2006', 'Active imobilizate 2006', 'Active circulante 2006', 'Capitaluri proprii 2006', 'Angajați (nr. mediu) 2006',
          'Cifra afaceri 2005', 'Profit Net 2005', 'Datorii 2005', 'Active imobilizate 2005', 'Active circulante 2005', 'Capitaluri proprii 2005', 'Angajați (nr. mediu) 2005']

req_headers={'Host': 'membri.listafirme.ro',
             'Connection': 'keep-alive',
             'Upgrade-Insecure-Requests': '1',
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
             'Sec-Fetch-Site': 'same-origin',
             'Sec-Fetch-Mode': 'navigate',
             'Sec-Fetch-Dest': 'document',
             'Accept-Encoding': 'gzip, deflate, br',
             'Accept-Language': 'en-US,en;q=0.9',
             'Cookie': '_ga=GA1.2.1704294020.1609922720; _gid=GA1.2.230116629.1609922720; __gads=ID=43fda99eebb485d9:T=1609922720:S=ALNI_MYc3mg3wjPhauQdUaLqfwUzNIpRwA; ASPSESSIONIDQUSTSQSB=FALMPMICDBPDBNAKOCLNIPLC; ASPSESSIONIDQWRSTQSB=HMHFKFDDBMJCAFCGLOKIBPEH; ASPSESSIONIDSUTQRSRC=EDLIFONDHKDPBBIOHHBLFFGP; _gat_gtag_UA_4163803_5=1'
             }

file = open('listafirmeSpiderSCRAPY.csv', 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(file, fieldnames=header)
writer.writeheader()


class listfirmeSpider(scrapy.Spider):
    name = 'listfirmspider'
    # driver = webdriver.Chrome()
    Company_url_list = []
    Company_headers_list = []

    def start_requests(self):
        # self.driver.get('https://www.listafirme.ro/pagini/p1.htm')
        # self.driver.find_element_by_id('rememlg').click()
        # self.driver.find_element_by_css_selector('form[name="login"] input[type="text"]').send_keys('p.cosmin2013@gmail.com')
        # self.driver.find_element_by_css_selector('form[name="login"] input[type="password"]').send_keys('Vaida1!')
        # self.driver.find_element_by_css_selector('.checkbox input[type="checkbox"]').click()
        # self.driver.find_element_by_css_selector('form[name="login"] input[type="submit"]').click()
        # try:
        #
        #     alert = self.driver.switch_to_alert()
        #     alert.accept()
        #
        # except:
        #
        #     print("no alert")
        # T_page = int((self.driver.find_element_by_css_selector('.pagination li a').text).split()[2])
        # C_Page = 1
        # while C_Page <= 1:
        #     self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #     self.driver.find_elements_by_css_selector('.pagination li a i')[-1].click()
        #     C_Page = C_Page + 1
        #     for li in self.driver.find_elements_by_css_selector('.table.table-bordered.table-hover.table-striped.table-white tbody tr td a[target="profil"]')[:1]:
        #         href = li.get_attribute('href')
        #         self.Company_url_list.append(href)
        # for url in self.Company_url_list:
        yield scrapy.Request(url='https://membri.listafirme.ro/prescon-group-development-srl-11223199/')

    def parse(self, response, **kwargs):
        item = dict()
        item['Nume firma'] = ''.join(response.css('#date-de-identificare tr td')[1].css('::text').extract()).strip()
        item['Cod Unic de Înregistrare'] = ''.join(response.css('#date-de-identificare tr td')[3].css('::text').extract()).strip()
        item['Nr. Înmatriculare'] = ''.join(response.css('#date-de-identificare tr td')[5].css('::text').extract()).strip()
        item['EUID'] = ''.join(response.css('#date-de-identificare tr td')[7].css('::text').extract()).strip()
        item['Data finantarii:'] = ''.join(response.css('#date-de-identificare tr td')[9].css('::text').extract()).strip()
        item['Observatii'] = ''.join(response.css('#date-de-identificare tr td')[11].css('::text').extract()).strip()
        item['Poziţia în Topul Firmelor 2020'] = ''
        item['Descrierea firmei'] = ''.join(response.css('#descriere-firma .descriere_firma::text').extract())
        item['Referiri in social media'] = ''
        item['Judet'] = response.css('#contact tr td')[1].css('::text').extract_first()
        item['Localitate/Sector'] = response.css('#contact tr td')[3].css('::text').extract_first().strip()
        item['Adresa'] = ''.join(response.css('#contact tr td')[5].css('::text').extract())
        item['Telefon'] = ''.join(response.css('#contact tr td')[7].css('::text').extract())
        item['Fax'] = ''.join(response.css('#contact tr td')[9].css('::text').extract())
        item['Mobil'] = ''.join(response.css('#contact tr td')[11].css('::text').extract())
        item['Email'] = ''
        item['Persoane din conducere'] = ''
        item['Adresa web'] = ''
        item['Cod CAEN'] = ''
        T_years_records = (''.join(response.css('#bilant table tr .text-center::text').extract())).replace('\r\n', ' ').strip().split()
        for i, year in enumerate(T_years_records):
            item[f'Cifra afaceri {year}'] = response.css('#bilant table tr')[i + 1].css('td.text-right')[0].css('::text').extract_first()
            item[f'Profit Net {year}'] = response.css('#bilant table tr')[i + 1].css('td.text-right')[1].css('::text').extract_first()
            item[f'Datorii {year}'] = response.css('#bilant table tr')[i + 1].css('td.text-right')[2].css('::text').extract_first()
            item[f'Active imobilizate {year}'] = response.css('#bilant table tr')[i + 1].css('td.text-right')[3].css('::text').extract_first()
            item[f'Active circulante {year}'] = response.css('#bilant table tr')[i + 1].css('td.text-right')[4].css('::text').extract_first()
            item[f'Capitaluri proprii {year}'] = response.css('#bilant table tr')[i + 1].css('td.text-right')[5].css('::text').extract_first()
            item[f'Angajați (nr. mediu) {year}'] = response.css('#bilant table tr')[i + 1].css('td.text-right')[6].css('::text').extract_first()

        writer.writerow(item)
        file.flush()


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(listfirmeSpider)
process.start()
