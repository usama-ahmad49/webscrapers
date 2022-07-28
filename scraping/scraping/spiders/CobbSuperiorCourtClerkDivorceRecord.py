try:
    from pkg_resources import get_distribution
    import pkg_resources.py2_warn
except ImportError:
    pass
import requests
import json
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

file_json=open('CobbSuperiorCourtClerkDivorceRecord.json','w')
file_json_list=[]


def getjsondata_ind_case(number):
    url='https://ctsearch.cobbsuperiorcourtclerk.com/CaseDetails/{}'.format(number)
    response=requests.get(url)
    resp = scrapy.Selector(text=response.content.decode('utf-8'))
    casenumber=int(resp.css('#resultheader .resultrow.resultrowleft h3')[0].css('::text').extract_first().split()[3])
    casename=resp.css('#resultheader .resultrow.resultrowleft h3')[1].css('::text').extract_first()
    judge=resp.css('#resultheader .resultrow.resultrowleft h3')[2].css('::text').extract_first().split(':')[1]
    casetype=resp.css('#resultheader .resultrow.resultrowleft h3')[3].css('::text').extract_first().split(':')[1]
    filingDate=resp.css('#resultheader .resultrow.resultrowleft h3')[4].css('::text').extract_first().split(':')[1]
    caseStatus=resp.css('#resultheader .resultrow.resultrowleft h3')[5].css('::text').extract_first().split(':')[1]
    dipositionDate=resp.css('#resultheader .resultrow.resultrowleft h3')[6].css('::text').extract_first().split(':')[1]
    datadict=dict()
    datadict['case_no'] = dict()
    datadict['case_no']['civil_case_no']=casenumber
    datadict['case_no']['case_name']=casename
    datadict['case_no']['judge'] = judge
    datadict['case_no']['case_type'] = casetype
    datadict['case_no']['filing_date'] = filingDate
    datadict['case_no']['status'] = caseStatus
    datadict['case_no']['diposition_date'] = dipositionDate
    datadict['case_no']['parties'] = []
    datadict['case_no']['pleadings'] = []
    datadict['case_no']['hearings'] = []
    datadict['case_no']['attorneys'] = []
    datadict['case_no']['service'] = []
    datadict['case_no']['appeals'] = []
    datadict['case_no']['costs'] = []
    datadict['case_no']['disposition'] = []
    for parties in resp.css('#data_1 .resultgroup .resultrow'):
        party_item = dict()
        party_item['party_type']=parties.css('div.resultcell:nth-child(2)::text').extract_first().strip()
        party_item['name'] = parties.css('div.resultcell:nth-child(3)::text').extract_first().strip()
        datadict['case_no']['parties'].append(party_item)

    for parties in resp.css('#data_1 .resultgroup .resultaltrow'):
        party_item = dict()
        party_item['party_type']=parties.css('div.resultcell:nth-child(2)::text').extract_first().strip()
        party_item['name'] = parties.css('div.resultcell:nth-child(3)::text').extract_first().strip()
        datadict['case_no']['parties'].append(party_item)

    for pleading in resp.css('#data_2 .resultgroup .resultrow'):
        pleading_item = dict()
        pleading_item['file_date']= pleading.css('div.resultcell:nth-child(3)::text').extract_first().strip()
        pleading_item['add_date']=pleading.css('div.resultcell:nth-child(4)::text').extract_first().strip()
        pleading_item['filling_party']=pleading.css('div.resultcell:nth-child(5)::text').extract_first().strip()
        pleading_item['type']=pleading.css('div.resultcell:nth-child(6)::text').extract_first().strip()
        pleading_item['CCFN']=pleading.css('div.resultcell:nth-child(7)::text').extract_first().strip()
        datadict['case_no']['pleadings'].append(pleading_item)

    for pleading in resp.css('#data_2 .resultgroup .resultaltrow'):
        pleading_item = dict()
        pleading_item['file_date']= pleading.css('div.resultcell:nth-child(3)::text').extract_first().strip()
        pleading_item['add_date']=pleading.css('div.resultcell:nth-child(4)::text').extract_first().strip()
        pleading_item['filling_party']=pleading.css('div.resultcell:nth-child(5)::text').extract_first().strip()
        pleading_item['type']=pleading.css('div.resultcell:nth-child(6)::text').extract_first().strip()
        pleading_item['CCFN']=pleading.css('div.resultcell:nth-child(7)::text').extract_first().strip()
        datadict['case_no']['pleadings'].append(pleading_item)

    for hearing in resp.css('#data_3 .resultgroup .resultrow'):
        hearing_item=dict()
        hearing_item['hearing_number'] = hearing.css('div.resultcell:nth-child(1)::text').extract_first().strip()
        hearing_item['judge'] = hearing.css('div.resultcell:nth-child(2)::text').extract_first().strip()
        hearing_item['hearing_date'] = hearing.css('div.resultcell:nth-child(3)::text').extract_first().strip().split()[0]
        hearing_item['hearing_time'] = hearing.css('div.resultcell:nth-child(3)::text').extract_first().strip().split()[1]
        hearing_item['type'] = hearing.css('div.resultcell:nth-child(4)::text').extract_first('').strip()
        hearing_item['action'] = hearing.css('div.resultcell:nth-child(5)::text').extract_first('').strip()
        hearing_item['notice_date'] = hearing.css('div.resultcell:nth-child(6)::text').extract_first('').strip()
        hearing_item['location'] = hearing.css('div.resultcell:nth-child(7)::text').extract_first('').strip()
        datadict['case_no']['hearings'].append(hearing_item)

    for hearing in resp.css('#data_3 .resultgroup .resultaltrow'):
        hearing_item=dict()
        hearing_item['hearing_number'] = hearing.css('div.resultcell:nth-child(1)::text').extract_first().strip()
        hearing_item['judge'] = hearing.css('div.resultcell:nth-child(2)::text').extract_first().strip()
        hearing_item['hearing_date'] = hearing.css('div.resultcell:nth-child(3)::text').extract_first().strip().split()[0]
        hearing_item['hearing_time'] = hearing.css('div.resultcell:nth-child(3)::text').extract_first().strip().split()[1]
        hearing_item['type'] = hearing.css('div.resultcell:nth-child(4)::text').extract_first('').strip()
        hearing_item['action'] = hearing.css('div.resultcell:nth-child(5)::text').extract_first('').strip()
        hearing_item['notice_date'] = hearing.css('div.resultcell:nth-child(6)::text').extract_first('').strip()
        hearing_item['location'] = hearing.css('div.resultcell:nth-child(7)::text').extract_first('').strip()
        datadict['case_no']['hearings'].append(hearing_item)

    for attorney in resp.css('#data_4 .resultgroup .resultrow'):
        attorney_item = dict()
        attorney_item['party_number'] = attorney.css('div.resultcell:nth-child(1)::text').extract_first().strip()
        attorney_item['name'] = attorney.css('div.resultcell:nth-child(2)::text').extract_first().strip()
        attorney_item['status'] = attorney.css('div.resultcell:nth-child(3)::text').extract_first().strip()
        attorney_item['attorney_address'] = ' '.join(''.join(attorney.css('div.resultcell:nth-child(4)::text').extract()).split())
        datadict['case_no']['attorneys'].append(attorney_item)

    for attorney in resp.css('#data_4 .resultgroup .resultaltrow'):
        attorney_item = dict()
        attorney_item['party_number'] = attorney.css('div.resultcell:nth-child(1)::text').extract_first().strip()
        attorney_item['name'] = attorney.css('div.resultcell:nth-child(2)::text').extract_first().strip()
        attorney_item['status'] = attorney.css('div.resultcell:nth-child(3)::text').extract_first().strip()
        attorney_item['attorney_address'] = ' '.join(''.join(attorney.css('div.resultcell:nth-child(4)::text').extract()).split())
        datadict['case_no']['attorneys'].append(attorney_item)

    for service in resp.css('#data_5 .resultgroup .resultrow'):
        service_item = dict()
        service_item['party_number']= service.css('div.resultcell:nth-child(1)::text').extract_first().strip()
        service_item['service_number']=service.css('div.resultcell:nth-child(2)::text').extract_first().strip()
        service_item['filed_date']=service.css('div.resultcell:nth-child(3)::text').extract_first().strip()
        service_item['service_type']=service.css('div.resultcell:nth-child(4)::text').extract_first().strip()
        service_item['service_date']=service.css('div.resultcell:nth-child(5)::text').extract_first().strip()
        service_item['pleading']=service.css('div.resultcell:nth-child(6)::text').extract_first().strip()
        service_item['CCFN']=service.css('div.resultcell:nth-child(7)::text').extract_first().strip()
        datadict['case_no']['service'].append(service_item)

    for service in resp.css('#data_5 .resultgroup .resultaltrow'):
        service_item = dict()
        service_item['party_number']= service.css('div.resultcell:nth-child(1)::text').extract_first().strip()
        service_item['service_number']=service.css('div.resultcell:nth-child(2)::text').extract_first().strip()
        service_item['filed_date']=service.css('div.resultcell:nth-child(3)::text').extract_first().strip()
        service_item['service_type']=service.css('div.resultcell:nth-child(4)::text').extract_first().strip()
        service_item['service_date']=service.css('div.resultcell:nth-child(5)::text').extract_first().strip()
        service_item['pleading']=service.css('div.resultcell:nth-child(6)::text').extract_first().strip()
        service_item['CCFN']=service.css('div.resultcell:nth-child(7)::text').extract_first().strip()
        datadict['case_no']['service'].append(service_item)

    for appeal in resp.css('#data_6 .resultgroup .resultrow'):
        appeal_item=dict()
        appeal_item['party_number']=appeal.css('div.resultcell:nth-child(1)::text').extract_first().strip()
        appeal_item['appealed_doc']=appeal.css('div.resultcell:nth-child(2)::text').extract_first().strip()
        appeal_item['date']=appeal.css('div.resultcell:nth-child(3)::text').extract_first().strip()
        appeal_item['court']=appeal.css('div.resultcell:nth-child(4)::text').extract_first().strip()
        datadict['case_no']['appeals'].append(appeal_item)

    for appeal in resp.css('#data_6 .resultgroup .resultaltrow'):
        appeal_item=dict()
        appeal_item['party_number']=appeal.css('div.resultcell:nth-child(1)::text').extract_first().strip()
        appeal_item['appealed_doc']=appeal.css('div.resultcell:nth-child(2)::text').extract_first().strip()
        appeal_item['date']=appeal.css('div.resultcell:nth-child(3)::text').extract_first().strip()
        appeal_item['court']=appeal.css('div.resultcell:nth-child(4)::text').extract_first().strip()
        datadict['case_no']['appeals'].append(appeal_item)

    for cost in resp.css('#data_7 .resultgroup .resultrow'):
        cost_item=dict()
        cost_item['party_number']=cost.css('div.resultcell:nth-child(1)::text').extract_first().strip()
        cost_item['cost_number']=cost.css('div.resultcell:nth-child(2)::text').extract_first().strip()
        cost_item['date']=cost.css('div.resultcell:nth-child(3)::text').extract_first().strip()
        cost_item['paid']=cost.css('div.resultcell:nth-child(4)::text').extract_first().strip()
        cost_item['refund']=cost.css('div.resultcell:nth-child(5)::text').extract_first().strip()
        cost_item['recipt_number']=cost.css('div.resultcell:nth-child(6)::text').extract_first().strip()
        datadict['case_no']['costs'].append(cost_item)

    for cost in resp.css('#data_7 .resultgroup .resultaltrow'):
        cost_item=dict()
        cost_item['party_number']=cost.css('div.resultcell:nth-child(1)::text').extract_first().strip()
        cost_item['cost_number']=cost.css('div.resultcell:nth-child(2)::text').extract_first().strip()
        cost_item['date']=cost.css('div.resultcell:nth-child(3)::text').extract_first().strip()
        cost_item['paid']=cost.css('div.resultcell:nth-child(4)::text').extract_first().strip()
        cost_item['refund']=cost.css('div.resultcell:nth-child(5)::text').extract_first().strip()
        cost_item['recipt_number']=cost.css('div.resultcell:nth-child(6)::text').extract_first().strip()
        datadict['case_no']['costs'].append(cost_item)

    for disposition in resp.css('#data_8 .resultgroup .resultrow'):
        disposition_item=dict()
        disposition_item['party_number']=disposition.css('div.resultcell:nth-child(1)::text').extract_first().strip()
        disposition_item['type']=disposition.css('div.resultcell:nth-child(2)::text').extract_first().strip()
        disposition_item['file_date']=disposition.css('div.resultcell:nth-child(3)::text').extract_first().strip()
        disposition_item['disp_date']=disposition.css('div.resultcell:nth-child(4)::text').extract_first().strip()
        disposition_item['nunc_pro_tunc']=disposition.css('div.resultcell:nth-child(5)::text').extract_first().strip()
        disposition_item['judge']=disposition.css('div.resultcell:nth-child(6)::text').extract_first().strip()
        disposition_item['CCFN']=disposition.css('div.resultcell:nth-child(7)::text').extract_first().strip()
        datadict['case_no']['disposition'].append(disposition_item)

    for disposition in resp.css('#data_8 .resultgroup .resultaltrow'):
        disposition_item=dict()
        disposition_item['party_number']=disposition.css('div.resultcell:nth-child(1)::text').extract_first().strip()
        disposition_item['type']=disposition.css('div.resultcell:nth-child(2)::text').extract_first().strip()
        disposition_item['file_date']=disposition.css('div.resultcell:nth-child(3)::text').extract_first().strip()
        disposition_item['disp_date']=disposition.css('div.resultcell:nth-child(4)::text').extract_first().strip()
        disposition_item['nunc_pro_tunc']=disposition.css('div.resultcell:nth-child(5)::text').extract_first().strip()
        disposition_item['judge']=disposition.css('div.resultcell:nth-child(6)::text').extract_first().strip()
        disposition_item['CCFN']=disposition.css('div.resultcell:nth-child(7)::text').extract_first().strip()
        datadict['case_no']['disposition'].append(disposition_item)
    file_json_list.append(datadict)







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
                getjsondata_ind_case(item['CaseNumber'])
            except:
                break
            try:
                item['Judge'] = resp.css('#resulthits #row_{} .resultcell.nowrap ::text'.format(i)).extract()[2:][2]
            except:
                break
            i=i+1
            writer.writerow(item)
            file.flush()
    # for dictionary in file_json_list:
    json.dump(fp=file_json,obj=file_json_list)


if __name__ == '__main__':
    getresults()