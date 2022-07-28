import time
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

if __name__ == '__main__':
    links = []
    options = Options()
    options.add_argument('--disable-notifications')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get('https://www.facebook.com/')
    driver.find_element_by_id('email').send_keys('123')
    driver.find_element_by_id('pass').send_keys('123')
    driver.find_element_by_css_selector("button[name='login']").click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="search"]')))
    time.sleep(3)
    driver.find_element_by_css_selector('input[type="search"]').send_keys('DHA Lahore Property Sale and Buy', Keys.ENTER)
    time.sleep(5)
    for re in driver.find_elements_by_css_selector('.rq0escxv.l9j0dhe7.du4w35lb.j83agx80.cbu4d94t.pfnyh3mw.d2edcug0.aahdfvyu.tvmbv18p a'):
        if 'Groups' in re.text:
            re.click()
            time.sleep(2)
            break
    link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[role="article"] .j83agx80 .hpfvmrgz.g5gj957u.buofh1pr.rj1gh0hx.o8rfisnq .qzhwtbm6.knvmm38d a'))).get_attribute('href')
    driver.get(link)
    time.sleep(3)
    for mem in driver.find_elements_by_css_selector('.soycq5t1.l9j0dhe7 .i09qtzwb.rq0escxv.n7fi1qx3.pmk7jnqg.j9ispegn.kr520xx4 a'):
        if 'Members' in mem.text:
            mem.click()
            time.sleep(3)
            break
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
    response = scrapy.Selector(text=driver.page_source)
    for res in response.css('.b20td4e0.muag1w35')[-1].css('div[data-visualcompletion="ignore-dynamic"]'):
        link  = f'https://www.facebook.com{res.css("a::attr(href)").extract_first("")}'
        links.append(link)
    print('this')

