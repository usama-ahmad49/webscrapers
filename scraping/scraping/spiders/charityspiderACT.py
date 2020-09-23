try:
    from pkg_resources import get_distribution
    import pkg_resources.py2_warn
except ImportError:
    pass

import datetime

import scrapy
from scrapy.crawler import CrawlerProcess
import csv

csv_columnsB1 = ["Page_URL", "ABN", "ABN_URL", "Name_of_the_Organization", "Address", "Email",
                 "Address_for_Email_Services", "Website",
                 "Phone_Number", "Charity_Size", "Who_the_Charity_Helps", "Date_Established", "Last_Reported",
                 "Next_Report_Due", "Financial_Year_End", "Summary_Of_Activities"]
csvfileB1 = open('B1_(ACT)Australian_Capital_Territory_Charity_Details.csv'.format(datetime.datetime.now().date()), 'w', newline='',
                 encoding="utf-8")
writer = csv.DictWriter(csvfileB1, fieldnames=csv_columnsB1)
writer.writeheader()
csv_columnsB2 = ["ABN", "Name_of_the_Organization", "Name_of_each_person", "Position_of_each_person"]
csvfileB2 = open('B2_(ACT)Australian_Capital_Territory_Charity_People_Details.csv'.format(datetime.datetime.now().date()), 'w', newline='',
                 encoding="utf-8")
Pople_Writer = csv.DictWriter(csvfileB2, fieldnames=csv_columnsB2)
Pople_Writer.writeheader()


class charityspiderACT(scrapy.Spider):
    name = 'charity'
    title = 'Charity'
    CONCURRENT_REQUESTS = 3
    DOWNLOAD_DELAY = 1

    def start_requests(self):

        for pageno in range(0,700):
            link='https://www.acnc.gov.au/charity?location%5B0%5D=266&page={}'.format(pageno)
            yield scrapy.Request(link, callback=self.parse, dont_filter=True)

    def parse(self, response):
        for charityLink in response.css('.views-field.views-field-acnc-search-api-title-sort a::attr(href)').extract()[1:]:
            # print('https://www.acnc.gov.au{}'.format(charityLink))
            yield scrapy.Request('https://www.acnc.gov.au{}'.format(charityLink), callback=self.parse_charity_details,
                                 dont_filter=True)


    def parse_charity_details(self, response):
        # for file B1
        item = dict()
        item['Page_URL'] = response.url
        item['ABN'] = response.css('.field.field-name-field-abn.field-type-text.field-label-inline.clearfix '
                                   '.field-item.even a ::text').extract_first()
        item['ABN_URL'] = response.css(
            '.field.field-name-field-abn.field-type-text.field-label-inline.clearfix .field-item.even a ::attr(href)').extract_first()
        item['Name_of_the_Organization'] = response.css(
            '.field.field-name-title.field-type-ds.field-label-hidden .field-item.even h1 ::text').extract_first()
        item['Address'] = ', '.join(response.css(
            '.field.field-name-field-address.field-type-addressfield.field-label-inline .clearfix '
            '.thoroughfare::text, .locality::text, .state::text, .postal-code::text, .country::text').extract())
        item['Email'] = response.css(
            '.field.field-name-field-email.field-type-text.field-label-inline.clearfix .field-item.even a::text').extract_first()
        item['Address_for_Email_Services'] = response.css(
            '.field.field-name-field-afs-email.field-type-text.field-label-inline.clearfix .field-item.even a::text').extract_first()
        item['Website'] = response.css(
            '.field.field-name-field-website.field-type-text.field-label-inline.clearfix .field-item.even a::attr(href)').extract_first()
        item['Phone_Number'] = response.css(
            '.field.field-name-field-phone.field-type-text.field-label-inline.clearfix .field-item.even a::text').extract_first()
        item['Charity_Size'] = response.css(
            '.field.field-name-field-charity-size.field-type-text.field-label-inline.clearfix .field-item.even ::text').extract_first()
        item['Who_the_Charity_Helps'] = response.css(
            '.field.field-name-field-beneficiaries.field-type-taxonomy-term-reference.field-label-inline.clearfix '
            '.field-item.even ::text').extract_first()
        item['Date_Established'] = response.css(
            '.field.field-name-field-date-established.field-type-datetime.field-label-inline.clearfix '
            '.date-display-single ::text').extract_first()
        item['Last_Reported'] = response.css(
            '.field.field-name-field-last-reported.field-type-datetime.field-label-inline.clearfix '
            '.date-display-single ::text').extract_first()
        item['Next_Report_Due'] = response.css(
            '.field.field-name-field-next-report-due.field-type-datetime.field-label-inline.clearfix '
            '.date-display-single ::text').extract_first()
        item['Financial_Year_End'] = response.css(
            '.field.field-name-field-financial-year-end.field-type-text.field-label-inline.clearfix .field-item.even '
            '::text').extract_first()
        item['Summary_Of_Activities'] = response.css(
            '.group-summary-activities.field-group-div .field-item.even ::text').extract_first()
        writer.writerow(item)
        csvfileB1.flush()
        # for file B2
        item2 = dict()
        item2['ABN'] = response.css('.field.field-name-field-abn.field-type-text.field-label-inline.clearfix '
                                    '.field-item.even a ::text').extract_first()
        item2['Name_of_the_Organization'] = response.css(
            '.field.field-name-title.field-type-ds.field-label-hidden .field-item.even h1 ::text').extract_first()
        item2['Name_of_each_person'] = ' , '.join(response.css(
            '.field.field-name-acnc-node-charity-people.field-type-ds.field-label-hidden '
            '.views-field.views-field-title h4 ::text').extract())
        item2['Position_of_each_person'] = ' , '.join(response.css(
            '.field.field-name-acnc-node-charity-people.field-type-ds.field-label-hidden '
            '.views-field.views-field-field-role p ::text').extract())

        Pople_Writer.writerow(item2)
        csvfileB2.flush()
        
        
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(charityspiderACT)
process.start()
