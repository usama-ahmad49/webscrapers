import scrapy
import csv
import requests
from threading import Thread
from urllib.parse import unquote


header = ["Name", "Email", "About", "skills", "Level of Availability", "Interesting links", "Location"]
file = open('HelpWithCovidSpider.csv', 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(file, fieldnames=header)
writer.writeheader()


def get_volunteers_data(url):
    item = dict()
    print(url)
    response = requests.get(url)
    resp = scrapy.Selector(text=response.text)
    item['Name'] = resp.css('.px-4.pb-5 .flex.items-center.flex-col.pb-4.pt-6 h3::text').extract_first().strip()
    emailstr = resp.css('dl div:nth-child(1) dd ::text').extract()[1].split("'")[1]
    item['Email'] = (unquote(emailstr).split('mailto:')[1]).split("'")[0]
    item['About'] = resp.css('dd p::text').extract_first().strip()
    try:
        item['skills'] = ''.join(resp.css('dd a::text').extract()[:-1]).replace('\n', '')
    except:
        item['skills'] = ''
    try:
        item['Level of Availability'] = resp.css('.px-4.pb-5 dl div:nth-child(4) dd::text').extract_first().strip()
    except:
        item['Level of Availability'] = ''
    item['Interesting links'] = ';'.join(resp.css('dd p a::text').extract())
    item['Location'] = resp.css('dd::text').extract()[-1].strip()

    writer.writerow(item)


def get_volunteers_links(url, links):
    resp = requests.get(url)
    response = scrapy.Selector(text=resp.text)
    for li in response.css('.mt-4 .flex-1.flex.flex-col.justify-between.p-5'):
        link = 'https://helpwithcovid.com' + li.css('.flex-col .text-indigo-500.text-lg.font-medium a::attr(href)').extract_first()
        links.append(link)


def get_total_pages(url):
    resp = requests.get(url)
    response = scrapy.Selector(text=resp.text)
    totalResults = int(response.css('.mt-4 .mb-4 p span:nth-child(3)::text').extract_first())
    pa = totalResults / 24
    if pa == 0:
        pages = pa
    else:
        pages = int(pa) + 1
    return pages


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


if __name__ == '__main__':
    links = []
    thread1 = []
    url = 'https://helpwithcovid.com/users'
    i = 1
    pages = get_total_pages(url)
    while i <= pages:
        url = 'https://helpwithcovid.com/users/p/{}'.format(i)
        i = i + 1
        # getvolunteerslinks(url, links)
        t = Thread(target=get_volunteers_links, args=(url, links))
        t.start()
        thread1.append(t)
    for t in thread1:
        t.join()
    for chunk_links in chunks(links, 10):
        thread2 = []
        for link in chunk_links:
            newt = Thread(target=get_volunteers_data, args=(link,))
            newt.start()
            thread2.append(newt)
        for newt in thread2:
            newt.join()
