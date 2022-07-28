import csv
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

import requests

header = ['Nume firma', 'Cod Unic de Înregistrare', 'Nr. Înmatriculare', 'EUID', 'Data finantarii:', 'Observatii', 'Poziţia în Topul Firmelor 2020', 'Descrierea firmei', 'Referiri in social media', 'Judet', 'Localitate/Sector', 'Adresa', 'Telefon', 'Fax', 'Mobil', 'Email', 'Persoane din conducere', 'Adresa web', 'Cod CAEN', 'Cifra afaceri 2019', 'Profit Net 2019', 'Datorii 2019', 'Active imobilizate 2019', 'Active circulante 2019', 'Capitaluri proprii 2019', 'Angajați (nr. mediu) 2019', 'Cifra afaceri 2018', 'Profit Net 2018', 'Datorii 2018', 'Active imobilizate 2018', 'Active circulante 2018', 'Capitaluri proprii 2018', 'Angajați (nr. mediu) 2018', 'Cifra afaceri 2017', 'Profit Net 2017', 'Datorii 2017', 'Active imobilizate 2017', 'Active circulante 2017', 'Capitaluri proprii 2017', 'Angajați (nr. mediu) 2017', 'Cifra afaceri 2016', 'Profit Net 2016', 'Datorii 2016',
          'Active imobilizate 2016', 'Active circulante 2016', 'Capitaluri proprii 2016', 'Angajați (nr. mediu) 2016', 'Cifra afaceri 2015', 'Profit Net 2015', 'Datorii 2015', 'Active imobilizate 2015', 'Active circulante 2015', 'Capitaluri proprii 2015', 'Angajați (nr. mediu) 2015', 'Cifra afaceri 2014', 'Profit Net 2014', 'Datorii 2014', 'Active imobilizate 2014', 'Active circulante 2014', 'Capitaluri proprii 2014', 'Angajați (nr. mediu) 2014', 'Cifra afaceri 2013', 'Profit Net 2013', 'Datorii 2013', 'Active imobilizate 2013', 'Active circulante 2013', 'Capitaluri proprii 2013', 'Angajați (nr. mediu) 2013', 'Cifra afaceri 2012', 'Profit Net 2012', 'Datorii 2012', 'Active imobilizate 2012', 'Active circulante 2012', 'Capitaluri proprii 2012', 'Angajați (nr. mediu) 2012', 'Cifra afaceri 2011', 'Profit Net 2011', 'Datorii 2011', 'Active imobilizate 2011', 'Active circulante 2011',
          'Capitaluri proprii 2011', 'Angajați (nr. mediu) 2011', 'Cifra afaceri 2010', 'Profit Net 2010', 'Datorii 2010', 'Active imobilizate 2010', 'Active circulante 2010', 'Capitaluri proprii 2010', 'Angajați (nr. mediu) 2010', 'Cifra afaceri 2009', 'Profit Net 2009', 'Datorii 2009', 'Active imobilizate 2009', 'Active circulante 2009', 'Capitaluri proprii 2009', 'Angajați (nr. mediu) 2009', 'Cifra afaceri 2008', 'Profit Net 2008', 'Datorii 2008', 'Active imobilizate 2008', 'Active circulante 2008', 'Capitaluri proprii 2008', 'Angajați (nr. mediu) 2008', 'Cifra afaceri 2007', 'Profit Net 2007', 'Datorii 2007', 'Active imobilizate 2007', 'Active circulante 2007', 'Capitaluri proprii 2007', 'Angajați (nr. mediu) 2007', 'Cifra afaceri 2006', 'Profit Net 2006', 'Datorii 2006', 'Active imobilizate 2006', 'Active circulante 2006', 'Capitaluri proprii 2006', 'Angajați (nr. mediu) 2006',
          'Cifra afaceri 2005', 'Profit Net 2005', 'Datorii 2005', 'Active imobilizate 2005', 'Active circulante 2005', 'Capitaluri proprii 2005', 'Angajați (nr. mediu) 2005', 'Cifra afaceri 2004', 'Profit Net 2004', 'Datorii 2004', 'Active imobilizate 2004', 'Active circulante 2004', 'Capitaluri proprii 2004', 'Angajați (nr. mediu) 2004', 'Cifra afaceri 2003', 'Profit Net 2003', 'Datorii 2003', 'Active imobilizate 2003', 'Active circulante 2003', 'Capitaluri proprii 2003', 'Angajați (nr. mediu) 2003', 'Cifra afaceri 2002', 'Profit Net 2002', 'Datorii 2002', 'Active imobilizate 2002', 'Active circulante 2002', 'Capitaluri proprii 2002', 'Angajați (nr. mediu) 2002', 'Cifra afaceri 2001', 'Profit Net 2001', 'Datorii 2001', 'Active imobilizate 2001', 'Active circulante 2001', 'Capitaluri proprii 2001', 'Angajați (nr. mediu) 2001', 'Cifra afaceri 2000', 'Profit Net 2000', 'Datorii 2000',
          'Active imobilizate 2000', 'Active circulante 2000', 'Capitaluri proprii 2000', 'Angajați (nr. mediu) 2000']

file = open('listafirmeSpider.csv', 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(file, fieldnames=header)
writer.writeheader()


def parse(driver):
    if 'Trafic neuzual pentru' in driver.find_element_by_xpath('/html/body/div[1]/main/section/div/h1').text:
        driver.find_element_by_css_selector('#btnSubmit').click()
        key = driver.find_element_by_xpath('//iframe[@title="testare reCAPTCHA"]').get_attribute('src').split('k=')[
            1].split('&cb')[0]
        url = 'https://2captcha.com/in.php?key=ff76791ce8d9daffc0c495ce02a2992b&method=userrecaptcha&googlekey={}&pageurl=https://membri.listafirme.ro/trafic-neuzual.asp'.format(
            key)
        resp = requests.get(url)
        time.sleep(5)
        resp1 = requests.get(
            'https://2captcha.com/res.php?key=ff76791ce8d9daffc0c495ce02a2992b&action=get&id={}'.format(
                resp.text.split('|')[1]))
        while not 'OK|' in resp1.text:
            time.sleep(5)
            resp1 = requests.get(
                'https://2captcha.com/res.php?key=ff76791ce8d9daffc0c495ce02a2992b&action=get&id={}'.format(
                    resp.text.split('|')[1]))
        token = resp1.text.split('OK|')[1]
        style = driver.find_element_by_id('g-recaptcha-response').get_attribute('style')
        style = style.replace(' resize: none; display: none;', '').strip()
        e = driver.find_element_by_id('g-recaptcha-response')
        driver.execute_script("arguments[0].setAttribute('style',arguments[1])", e, '')
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'g-recaptcha-response'))
        )  # Wait until the `text_to_score` element appear (up to 5 seconds)
        actions = ActionChains(driver)
        actions.move_to_element(e).perform()
        driver.find_element_by_id('g-recaptcha-response').send_keys(token)
        driver.find_element_by_id('g-recaptcha-response').submit()
    item = dict()
    item['Nume firma'] = driver.find_elements_by_css_selector('#date-de-identificare tr td')[1].text
    item['Cod Unic de Înregistrare'] = driver.find_elements_by_css_selector('#date-de-identificare tr td')[3].text
    item['Nr. Înmatriculare'] = driver.find_elements_by_css_selector('#date-de-identificare tr td')[5].text
    item['EUID'] = driver.find_elements_by_css_selector('#date-de-identificare tr td')[7].text
    item['Data finantarii:'] = driver.find_elements_by_css_selector('#date-de-identificare tr td')[9].text
    item['Observatii'] = driver.find_elements_by_css_selector('#date-de-identificare tr td')[11].text
    if 'în Topul Firmelor' in driver.find_element_by_xpath('/html/body/div[1]/main/section/div/table[1]/tbody/tr[1]/th').text:
        item['Poziţia în Topul Firmelor 2020'] = driver.find_element_by_xpath('/html/body/div[1]/main/section/div/table[1]/tbody/tr[2]/td').text
    try:
        item['Descrierea firmei'] = driver.find_element_by_css_selector('#descriere-firma .descriere_firma').text
    except:
        pass

    social_urls = []
    for i in driver.find_elements_by_xpath('/html/body/div[1]/main/section/div/table[4]/tbody/tr[2]/td/a'):
        social_urls.append(i.get_attribute('href'))
    item['Referiri in social media'] = '  '.join(social_urls)
    item['Judet'] = driver.find_elements_by_css_selector('#contact tr td')[1].text
    item['Localitate/Sector'] = driver.find_elements_by_css_selector('#contact tr td')[3].text
    item['Adresa'] = driver.find_elements_by_css_selector('#contact tr td')[5].text
    item['Telefon'] = driver.find_elements_by_css_selector('#contact tr td')[7].text
    item['Fax'] = driver.find_elements_by_css_selector('#contact tr td')[9].text
    item['Mobil'] = driver.find_elements_by_css_selector('#contact tr td')[11].text
    item['Email'] = driver.find_elements_by_css_selector('#contact tr td')[13].text.replace('\n',' ')
    item['Persoane din conducere'] = driver.find_elements_by_css_selector('#contact tr td')[15].text.replace('\n',' ')
    item['Adresa web'] = driver.find_elements_by_css_selector('#contact tr td')[17].text.replace('\n',' ')
    item['Cod CAEN'] = driver.find_elements_by_css_selector('#domeniu-de-activitate tr td')[1].text
    T_years = []
    for i in driver.find_elements_by_css_selector('#bilant table tr td.text-center')[:-1]:
        T_years.append(int(i.text))
    for i, year in enumerate(T_years):
        item[f'Cifra afaceri {year}'] = driver.find_elements_by_css_selector('#bilant table tr')[i + 1].find_elements_by_css_selector('td.text-right')[0].text
        item[f'Profit Net {year}'] = driver.find_elements_by_css_selector('#bilant table tr')[i + 1].find_elements_by_css_selector('td.text-right')[1].text
        item[f'Datorii {year}'] = driver.find_elements_by_css_selector('#bilant table tr')[i + 1].find_elements_by_css_selector('td.text-right')[2].text
        item[f'Active imobilizate {year}'] = driver.find_elements_by_css_selector('#bilant table tr')[i + 1].find_elements_by_css_selector('td.text-right')[3].text
        item[f'Active circulante {year}'] = driver.find_elements_by_css_selector('#bilant table tr')[i + 1].find_elements_by_css_selector('td.text-right')[4].text
        item[f'Capitaluri proprii {year}'] = driver.find_elements_by_css_selector('#bilant table tr')[i + 1].find_elements_by_css_selector('td.text-right')[5].text
        item[f'Angajați (nr. mediu) {year}'] = driver.find_elements_by_css_selector('#bilant table tr')[i + 1].find_elements_by_css_selector('td.text-right')[6].text

    driver.close()
    writer.writerow(item)
    file.flush()


if __name__ == '__main__':
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Start Time =", current_time)
    options = Options()
    options.add_argument('--disable-notifications')
    driver = webdriver.Chrome(chrome_options=options)
    driver.maximize_window()
    driver.get('https://membri.listafirme.ro/pagini/p1.htm')
    if 'https://www.listafirme.ro/trafic-neuzual.asp' in driver.current_url:
        time.sleep(3)
        driver.find_element_by_css_selector('#btnSubmit').click()
        key = driver.find_element_by_xpath('//iframe[@title="testare reCAPTCHA"]').get_attribute('src').split('k=')[
            1].split('&cb')[0]
        url = 'https://2captcha.com/in.php?key=ff76791ce8d9daffc0c495ce02a2992b&method=userrecaptcha&googlekey={}&pageurl=https://membri.listafirme.ro/trafic-neuzual.asp'.format(
            key)
        resp = requests.get(url)
        time.sleep(5)
        resp1 = requests.get(
            'https://2captcha.com/res.php?key=ff76791ce8d9daffc0c495ce02a2992b&action=get&id={}'.format(
                resp.text.split('|')[1]))
        while not 'OK|' in resp1.text:
            time.sleep(5)
            resp1 = requests.get(
                'https://2captcha.com/res.php?key=ff76791ce8d9daffc0c495ce02a2992b&action=get&id={}'.format(
                    resp.text.split('|')[1]))
        token = resp1.text.split('OK|')[1]
        style = driver.find_element_by_id('g-recaptcha-response').get_attribute('style')
        style = style.replace(' resize: none; display: none;', '').strip()
        e = driver.find_element_by_id('g-recaptcha-response')
        driver.execute_script("arguments[0].setAttribute('style',arguments[1])", e, '')
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'g-recaptcha-response'))
        )  # Wait until the `text_to_score` element appear (up to 5 seconds)
        actions = ActionChains(driver)
        actions.move_to_element(e).perform()
        driver.find_element_by_id('g-recaptcha-response').send_keys(token)
        driver.find_element_by_id('g-recaptcha-response').submit()

    driver.find_element_by_id('rememlg').click()
    driver.find_element_by_css_selector('form[name="login"] input[type="text"]').send_keys('p.cosmin2013@gmail.com')
    driver.find_element_by_css_selector('form[name="login"] input[type="password"]').send_keys('Vaida1!')
    driver.find_element_by_css_selector('.checkbox input[type="checkbox"]').click()
    driver.find_element_by_css_selector('form[name="login"] input[type="submit"]').click()
    try:
        alert = driver.switch_to_alert()
        alert.accept()
    except:
        print("no alert")
    time.sleep(5)
    # T_page = int((driver.find_element_by_css_selector('.pagination li a').text).split()[2])
    C_Page = 1
    while C_Page <= 1001:
        C_Page = C_Page + 1
        for i, li in enumerate(driver.find_elements_by_css_selector('.table.table-bordered.table-hover.table-striped.table-white tbody tr td a[target="profil"]')):
            got = False
            while not got:
                try:
                    li.click()
                    got = True
                except:
                    time.sleep(1)
            # driver.get('https://membri.listafirme.ro/trafic-neuzual.asp?url=/tck-centrum-srl-10881870/')
            driver._switch_to.window(window_name=driver.window_handles[-1])
            parse(driver)
            driver._switch_to.window(window_name=driver.window_handles[0])
            driver.execute_script("window.scrollTo(1, document.body.scrollHeight);")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        got = False
        while not got:
            try:
                driver.find_elements_by_css_selector('.pagination li a i')[-1].click()
                got = True
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print("Current Time =", current_time)
            except:
                time.sleep(1)

    driver.quit()
