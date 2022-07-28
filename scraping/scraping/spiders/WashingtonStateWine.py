try:
    from pkg_resources import get_distribution
    import pkg_resources.py2_warn
except ImportError:
    pass
import csv
import json
import boto3

import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import date
from botocore.exceptions import NoCredentialsError

ACCESS_KEY = 'AKIATJDQP5LAHRBHRAXE'
SECRET_KEY = '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'
BUCKET = 'winesofwashingtonstate'

headers = ["name", "winery-url", "imageUrl", "description", "socials", "Contact-Website", "Contact-Email", "Contact-Phone", "Contact-Address", "Contact-Region", "Contact-Contact", "wine-name", "wine-overview", "wine-photo", "wine-variety", "wine-Price-Range", "wine-AVA", "wine-list", "variety-list", "our story"]
filename = 'WashingtonStateWine {}.json'.format(date.today())
fileinput = open(filename, 'w')
# writer = csv.DictWriter(fileinput, fieldnames=headers)


class washingtonstatewine(scrapy.Spider):
    name = 'washingtonstatewine'

    @staticmethod
    def get_dict_value(data, key_list, default=''):
        """
        gets a dictionary and key_list, apply key_list sequentially on dictionary and return value
        :param data: dictionary
        :param key_list: list of key
        :param default: return value if key not found
        :return:
        """
        for key in key_list:
            if data and isinstance(data, dict):
                data = data.get(key, default)
            else:
                return default
        return data

    def start_requests(self):
        url = 'https://www.washingtonwine.org/api/queries/entities?limit=1&getcount=true&types=Winery&getwines=true&getlogo=true&getregion=true&query='
        yield scrapy.Request(url=url)

    def parse(self, response):
        json_text = response.text
        json_data = json.loads(json_text)
        total_count = self.get_dict_value(json_data, ['resultCount'])
        all_winery_urls = 'https://www.washingtonwine.org/api/queries/entities?limit={}&getcount=true&types=Winery&getwines=true&getlogo=true&getregion=true&query='.format(total_count)
        yield scrapy.Request(url=all_winery_urls, callback=self.parse_ind_winery_data)

    def parse_ind_winery_data(self, response):
        winery_url_list = []
        json_text = response.text
        json_data = json.loads(json_text)
        for data in self.get_dict_value(json_data, ['data'], []):
            allwinery_url = data.get('profileUrl')
            winery_url_list.append(allwinery_url)
        for url in winery_url_list:
            yield scrapy.Request(url=url, callback=self.parse_winery)

    def parse_winery(self, response):
        for wine_data in [v for v in response.css('.section.wines-panel.uk-flex.uk-flex-center .uk-flex.slideshow .uk-slideshow li') if v.css('h2')]:
            item = dict()
            item['name'] = response.css('#entity-cover div div h1::text').extract_first().strip()
            item['winery-url'] = response.url
            item['imageUrl'] = response.css('#entity-cover div div figure img::attr(src)').extract_first().strip()
            try:
                item['description'] = response.css('.section.profile-info .uk-flex.about p::text').extract_first().strip()
            except:
                item['description'] = ''
            item['socials'] = '; '.join(response.css('.section.profile-info .uk-flex.uk-flex-column.uk-width-large-3-10 div a ::attr(href)').extract())
            for resp in response.css('.section.profile-contact-details .uk-flex.uk-width-large-2-6.uk-flex-column.contact .uk-flex'):
                if resp.css('label::text').extract_first().strip() == 'Website':
                    item['Contact-Website'] = resp.css('a::attr(href)').extract_first().strip()
                elif resp.css('label::text').extract_first().strip() == 'Email':
                    item['Contact-Email'] = resp.css('a::attr(href)').extract_first().strip().replace('mailto:','')
                elif resp.css('label::text').extract_first().strip() == 'Phone':
                    item['Contact-Phone'] = resp.css('a::text').extract_first().strip()
                elif resp.css('label::text').extract_first().strip() == 'Address':
                    item['Contact-Address'] = ', '.join(resp.css('address a::text').extract())
                elif resp.css('label::text').extract_first().strip() == 'Region':
                    item['Contact-Region'] = resp.css('div::text').extract_first().strip()
                elif resp.css('label::text').extract_first().strip() == 'Contact':
                    item['Contact-Contact'] = resp.css('a::attr(href)').extract_first().strip()

            item['wine-name'] = wine_data.css('h2.uk-width-2-3.uk-width-large-7-10::text').extract_first().strip()
            item['wine-overview'] = wine_data.css('.uk-flex.slide-details .uk-width-large-2-3 .uk-switcher li p::text').extract_first()
            item['wine-photo'] = wine_data.css('.uk-flex.slide-details .uk-width-1-2.uk-width-medium-1-3 figure img::attr(src)').extract_first()
            for re in wine_data.css('.uk-flex.slide-details .uk-width-large-2-3 .uk-switcher li ul.description-list.uk-list.body-text li'):
                if re.css('label::text').extract_first() == 'Variety/Blend':
                    item['wine-variety'] = re.css('span::text').extract_first()
                elif re.css('label::text').extract_first() == 'Price Range':
                    item['wine-Price-Range'] = re.css('span::text').extract_first()
                elif re.css('label::text').extract_first() == 'AVA':
                    item['wine-AVA'] = re.css('span::text').extract_first()
            item['wine-list'] = '; '.join(response.css('.section.wines-panel.uk-flex.uk-flex-center .uk-width-large-1-3.uk-flex.uk-flex-column #profile-details .uk-list.tab-list li a::text').extract())
            item['variety-list'] = '; '.join(response.css('.section.wines-panel.uk-flex.uk-flex-center .uk-width-large-1-3.uk-flex.uk-flex-column #profile-details .uk-list.body-text li ::text').extract())
            try:
                item['our story'] = response.css('.section.text-photo-carousel article ::text').extract_first().strip()
            except:
                item['our story'] = ''
            # writer.writerow(item)
            # fileinput.flush()
            json_object=json.dumps(item, indent=20)
            fileinput.write(json_object)

    def close(spider, reason):
        s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
        try:
            s3.upload_file(filename, BUCKET, filename)
            print("Upload Successful")
            return True
        except FileNotFoundError:
            print("The file was not found")
            return False
        except NoCredentialsError:
            print("Credentials not available")
            return False


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(washingtonstatewine)
process.start()
