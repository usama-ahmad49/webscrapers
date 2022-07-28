import json
import csv
import requests
import scrapy
from scrapy.crawler import CrawlerProcess
import logging

headers = ['Venue Group', 'Venue Name', 'City', 'Country', 'Full Address']
fileinputcsv = open('ausvenueco.csv', 'w',encoding='utf-8', newline='')
csvwriter = csv.DictWriter(fileinputcsv, fieldnames=headers)
csvwriter.writeheader()

if __name__ == '__main__':
    url = 'https://www.ausvenueco.com.au/wp-admin/admin-ajax.php?action=venues_search&currentCategory=&showAllVenues=1'
    response = requests.get(url)
    Jdata = json.loads(response.content.decode('utf-8'))
    for dt in Jdata['venues_all']:
        item = dict()
        item['Venue Group'] = 'ausvenueco'
        item['Venue Name'] = dt['title']
        item['City'] = dt['suburb']
        item['Country'] = 'Australia'
        item['Full Address'] = dt['address'].replace('<br />', ' ').replace('\r', '').replace('\n', ' ')
        csvwriter.writerow(item)
        fileinputcsv.flush()
