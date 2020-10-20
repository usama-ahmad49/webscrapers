try:
    from pkg_resources import get_distribution
    import pkg_resources.py2_warn
except ImportError:
    pass
import requests
import scrapy
import copy
import csv
from socket import timeout


csvheader=["Plaintiff","Defendant","CaseType","CaseTitle","FileDate","CaseNumber","Judge"]
file=open('CobbSuperiorCourtClerkDivorceRecord.csv','w',newline='',encoding='utf-8')
writer=csv.DictWriter(file,fieldnames=csvheader)
writer.writeheader()

headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'accept-encoding': 'gzip, deflate, br',
           'accept-language': 'en-US,en;q=0.9',
           'cache-control': 'no-cache',
           'content-length': '223',
           'content-type': 'application/x-www-form-urlencoded',
           'cookie': 'PHPSESSID=8naqp3kuo759iofspb8vi4h1of',
           'origin': 'https://ctsearch.cobbsuperiorcourtclerk.com',
           'pragma': 'no-cache',
           'referer': 'https://ctsearch.cobbsuperiorcourtclerk.com/Results',
           'sec-fetch-dest': 'document',
           'sec-fetch-mode': 'navigate',
           'sec-fetch-site': 'same-origin',
           'sec-fetch-user': '?1',
           'upgrade-insecure-requests': '1',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
           }

FormData = {'resultrows': '100',
            'casetype': '516',
            'civcrim': 'civil',
            'daterange': 'thirtydays',
            'searchtype': 'CASETYPE',
            'goodthru': '10/15/2020',
            'datefrom': '2020-09-15',
            'datethru': '2020-10-15',
            'civthru': '2020-10-15',
            'crimthru': '2020-10-16',
            'offset': 0,
            'maxresults': '100',
            'resultrows2': '100'
            }


def getresults():
    data = copy.deepcopy(FormData)
    url = 'https://ctsearch.cobbsuperiorcourtclerk.com/Results'
    data['offset'] = -100
    while True:
        data['offset'] = data['offset'] + 100
        print(data['offset'])
        try:
            response = requests.post(url, headers=headers, data=data)
            resp = scrapy.Selector(text=response.content.decode('utf-8'))
            if not resp.css('#resulthits #row_0'):
                break
        except timeout:
            return
        i = 0
        while i < 100:
            item = dict()
            try:
                item['Plaintiff'] = ' '.join(resp.css('#resulthits #row_{} #name_{} ::text'.format(i, i)).extract_first().split(' ')[:4])
            except:
                break
            try:
                item['Defendant'] = ' '.join(resp.css('#resulthits #row_{} #othername_{} ::text'.format(i, i)).extract_first().split(' ')[:4])
            except:
                break
            try:
                item['CaseType'] = resp.css('#resulthits #row_{} .resultcell.nowrap ::text'.format(i)).extract()[2:][0].strip()
            except:
                break
            try:
                item['CaseTitle'] = resp.css('#resulthits #row_{} .resultcell #title_{}::text'.format(i,i)).extract_first().strip()
            except:
                break
            try:
                item['FileDate'] =resp.css('#resulthits #row_{} .resultcell.nowrap ::text'.format(i)).extract()[2:][1]
            except:
                break
            try:
                item['CaseNumber'] = resp.css('#resulthits #row_{} .resultcell ::text'.format(i)).extract()[3:][10]
            except:
                break
            try:
                item['Judge'] = resp.css('#resulthits #row_{} .resultcell.nowrap ::text'.format(i)).extract()[2:][2]
            except:
                break
            i=i+1
            writer.writerow(item)
            file.flush()


if __name__ == '__main__':
    getresults()
