from seleniumwire import webdriver
import csv
import json
import requests
import time


if __name__ == '__main__':
    csv_header=["When posted?","name","service","city","state","zipcode","phone number","Email","credits","question 1","question 2","question 3","question 4","question 5","question 6","Answer 1","Answer 2","Answer 3","Answer 4","Answer 5","Answer 6"]
    file_output=open('bark.csv','w',newline='',encoding='utf-8')
    writer = csv.DictWriter(file_output,fieldnames=csv_header)
    writer.writeheader()
    driver = webdriver.Firefox()
    driver.get('https://www.bark.com/sellers/dashboard/')
    driver.find_element_by_name('email').send_keys('barklead2020@gmail.com')
    driver.find_element_by_name('password').send_keys('kawzway2020')
    driver.find_element_by_class_name('btn.bark-btn.btn-primary.full-width').click()
    time.sleep(2)
    driver.get('https://www.bark.com/sellers/dashboard/')
    req = [v for v in driver.requests if 'ilter_counts=true' in v.path][0]
    json_data=json.loads(req.response.body)
    total_pages=json_data.get('data').get('last_page')
    headers=dict(req.headers)
    driver.close()
    for J_item in json_data.get('data').get('items'):
        item=dict()
        item['When posted?']=J_item.get('since')
        item['name'] = J_item.get('buyer_share_name')
        item['service'] = J_item.get('project_title')
        try:
            item['city'] = J_item.get('city_string').split()[0]
        except:
            item['city'] = ''
        try:
            item['state'] = J_item.get('city_string').split()[1]
        except:
            item['state'] = ''
        try:
            item['zipcode'] = J_item.get('city_string').split()[2]
        except:
            item['zipcode'] = ''
        item['phone number']=J_item.get('buyer_telephone')
        item['Email']=J_item.get('buyer_email')
        item['credits']=J_item.get('credits_required_original')
        try:
            item['question 1']=J_item.get('custom_fields')[0].get('question')
        except:
            item['question 1']=''
        try:
            item['question 2']=J_item.get('custom_fields')[1].get('question')
        except:
            item['question 2']=''
        try:
            item['question 3']=J_item.get('custom_fields')[2].get('question')
        except:
            item['question 3']=''
        try:
            item['question 4']=J_item.get('custom_fields')[3].get('question')
        except:
            item['question 4']=''
        try:
            item['question 5']=J_item.get('custom_fields')[4].get('question')
        except:
            item['question 5']=''
        try:
            item['question 6']=J_item.get('custom_fields')[5].get('question')
        except:
            item['question 6']=''
        try:
            item['Answer 1'] = J_item.get('custom_fields')[0].get('answer')
        except:
            item['Answer 1'] =''
        try:
            item['Answer 2'] = J_item.get('custom_fields')[1].get('answer')
        except:
            item['Answer 2'] = ''
        try:
            item['Answer 3'] = J_item.get('custom_fields')[2].get('answer')
        except:
            item['Answer 3'] = ''
        try:
            item['Answer 4'] = J_item.get('custom_fields')[3].get('answer')
        except:
            item['Answer 4'] = ''
        try:
            item['Answer 5'] = J_item.get('custom_fields')[4].get('answer')
        except:
            item['Answer 5'] = ''
        try:
            item['Answer 6'] = J_item.get('custom_fields')[5].get('answer')
        except:
            item['Answer 6'] = ''
        writer.writerow(item)
        file_output.flush()
    nextpage=json_data.get('data').get('next_page')
    i=1
    while i<total_pages:
        url='https://api.bark.com/seller/barks/?show_filter_counts=true&next_page={}&date%5B%5D=all&loid%5B%5D=any'.format(nextpage)
        response=requests.get(url=url, headers=headers)
        json_data=json.loads(response.content.decode('utf-8'))
        for J_item in json_data.get('data').get('items'):
            item = dict()
            item['When posted?'] = J_item.get('since')
            item['name'] = J_item.get('buyer_share_name')
            item['service'] = J_item.get('project_title')
            try:
                item['city'] = J_item.get('city_string').split()[0]
            except:
                item['city'] = ''
            try:
                item['state'] = J_item.get('city_string').split()[1]
            except:
                item['state'] = ''
            try:
                item['zipcode'] = J_item.get('city_string').split()[2]
            except:
                item['zipcode'] = ''
            item['phone number'] = J_item.get('buyer_telephone')
            item['Email'] = J_item.get('buyer_email')
            item['credits'] = J_item.get('credits_required_original')
            try:
                item['question 1'] = J_item.get('custom_fields')[0].get('question')
            except:
                item['question 1'] = ''
            try:
                item['question 2'] = J_item.get('custom_fields')[1].get('question')
            except:
                item['question 2'] = ''
            try:
                item['question 3'] = J_item.get('custom_fields')[2].get('question')
            except:
                item['question 3'] = ''
            try:
                item['question 4'] = J_item.get('custom_fields')[3].get('question')
            except:
                item['question 4'] = ''
            try:
                item['question 5'] = J_item.get('custom_fields')[4].get('question')
            except:
                item['question 5'] = ''
            try:
                item['question 6'] = J_item.get('custom_fields')[5].get('question')
            except:
                item['question 6'] = ''
            try:
                item['Answer 1'] = J_item.get('custom_fields')[0].get('answer')
            except:
                item['Answer 1'] = ''
            try:
                item['Answer 2'] = J_item.get('custom_fields')[1].get('answer')
            except:
                item['Answer 2'] = ''
            try:
                item['Answer 3'] = J_item.get('custom_fields')[2].get('answer')
            except:
                item['Answer 3'] = ''
            try:
                item['Answer 4'] = J_item.get('custom_fields')[3].get('answer')
            except:
                item['Answer 4'] = ''
            try:
                item['Answer 5'] = J_item.get('custom_fields')[4].get('answer')
            except:
                item['Answer 5'] = ''
            try:
                item['Answer 6'] = J_item.get('custom_fields')[5].get('answer')
            except:
                item['Answer 6'] = ''
            writer.writerow(item)
            file_output.flush()
        nextpage = json_data.get('data').get('next_page')
        i=i+1




    # for el in driver.find_element_by_class_name('dashboard-projects-item'):
    #     el.click()
    #     time.sleep(2)
    #     response=scrapy.Selector(driver.page_source)
    #     item=dict()
    #     item['When posted?'] = response.css('.posted-ago.for-leads.text-xs.text-light-grey.pt-2::text').extract_first()
    #     item['name'] = response.css('.project-name-location.pr-3.pt-2 .buyer_name::text').extract_first()
    #     item['service'] = response.css('.project-title.strong.mb-0.lh-md::text').extract_first()
    #     item['city'] = response.css('.project-name-location span::text').extract_first().split()[0]
    #     item['state']=response.css('.project-name-location span::text').extract_first().split()[1]
    #     item['zipcode']=response.css('.project-name-location span::text').extract_first().split()[2]
    #     item['phone number']=response.css('.buyer-telephone-display::text').extract_first()
    #     item['Email']=response.css('.buyer-email-display.text-break::text').extract_first()
    #     item['credits']=response.css('.num-credits-resp pl-2.text-grey-400::text').extract_first()
    #     # totalquestion=len(response.css('.project-questions-answers .project-details-question.text-xs.text-light-grey.pb-2'))
    #     item['question 1']=response.css('.project-questions-answers .project-details-question.text-xs.text-light-grey.pb-2::text').extract()[0]
    #     item['question 2']=response.css('.project-questions-answers .project-details-question.text-xs.text-light-grey.pb-2::text').extract()[1]
    #     item['question 3']=response.css('.project-questions-answers .project-details-question.text-xs.text-light-grey.pb-2::text').extract()[2]
    #     item['question 4']=response.css('.project-questions-answers .project-details-question.text-xs.text-light-grey.pb-2::text').extract()[3]
    #     item['question 5']=response.css('.project-questions-answers .project-details-question.text-xs.text-light-grey.pb-2::text').extract()[4]
    #     item['question 6']=response.css('.project-questions-answers .project-details-question.text-xs.text-light-grey.pb-2::text').extract()[5]
    #     item['Answer 1'] = response.css('.project-questions-answers .project-details-answer.text-xs.pb-4::text').extract()[0]
    #     item['Answer 2'] = response.css('.project-questions-answers .project-details-answer.text-xs.pb-4::text').extract()[1]
    #     item['Answer 3'] = response.css('.project-questions-answers .project-details-answer.text-xs.pb-4::text').extract()[2]
    #     item['Answer 4'] = response.css('.project-questions-answers .project-details-answer.text-xs.pb-4::text').extract()[3]
    #     item['Answer 5'] = response.css('.project-questions-answers .project-details-answer.text-xs.pb-4::text').extract()[4]
    #     item['Answer 6'] = response.css('.project-questions-answers .project-details-answer.text-xs.pb-4::text').extract()[5]