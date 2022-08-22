import time
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

if __name__ == '__main__':
    with open('facebookpasword.txt','r',encoding = 'utf-8') as userpwdfile:
        userpass = userpwdfile.read()
        username = userpass.split('\n')[0].strip()
        password = userpass.split('\n')[1].strip()
    with open('Keywordsfile.txt','r',encoding='utf-8') as keywordsfile:
        Keywords = keywordsfile.read().split('\n')
    options = Options()
    options.add_argument('--disable-notifications')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get('https://www.facebook.com/')
    driver.find_element(By.ID,'email').send_keys(username)
    driver.find_element(By.ID,'pass').send_keys(password)
    driver.find_element(By.CSS_SELECTOR,"button[name='login']").click()
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="search"]')))
    time.sleep(3)

    for keyword in Keywords:
        driver.find_element(By.CSS_SELECTOR,'input[aria-label="Search Facebook"]').click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Search Facebook"]').clear()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Search Facebook"]').send_keys(keyword)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Search Facebook"]').send_keys(Keys.ENTER)
        time.sleep(1)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                    '#mount_0_0_vd > div > div:nth-child(1) > div > div.bdao358l.om3e55n1.g4tp4svg > div > div > div > div.alzwoclg.cqf1kptm.p1t2w4gn.fawcizw8.om3e55n1.g4tp4svg > div.bdao358l.jez8cy9q.t5n4vrf6.o9w3sbdw.sr926ui1.jl2a5g8c.alzwoclg.cgu29s5g.fawcizw8.om3e55n1.g4tp4svg.qkxw7tbt > div.bdao358l.om3e55n1.alzwoclg.cqf1kptm.gvxzyvdx.aeinzg81.jez8cy9q.fawcizw8.sl4bvocy.mm98tyaj.b0ur3jhr > div > div.r7ybg2qv.qbc87b33.jk4gexc9.alzwoclg.cqf1kptm.lq84ybu9.g4tp4svg.ly56v2vv.h67akvdo.ir1gxh3s.sqler345.by1hb0a5.thmcm15y.cgu29s5g.i15ihif8.dnr7xe2t.id4k59z1.jfw19y2w.b95sz57d.mm05nxu8.izce65as.om3e55n1.qbfhvn0q > div.alzwoclg.cqf1kptm.cgu29s5g.om3e55n1 > div.th51lws0 > div > div > div:nth-child(2) > div > div:nth-child(1)')))
        PostElem = [v for v in driver.find_elements(By.CSS_SELECTOR, 'div[role="list"] div[role="listitem"]') if
         v.text == 'Posts'][0]
        PostElem.click()
        time.sleep(3)

        last_height = driver.execute_script("return document.body.scrollHeight")
        i = 0
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            i += 1
            if i == 20:
                i = 0
                # time.sleep(1)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height




