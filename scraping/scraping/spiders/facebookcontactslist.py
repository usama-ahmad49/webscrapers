try:
    from pkg_resources import get_distribution
    import pkg_resources.py2_warn
except ImportError:
    pass

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


if __name__ == '__main__':
    fileinput = open('usernameFacebook.txt','r')
    infile = fileinput.read().split('\n')
    file = open('listofcontacts.txt','w')
    url = 'https://www.facebook.com/'
    options = Options()
    options.add_argument('--disable-notifications')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'email')))
    time.sleep(2)
    driver.find_element_by_id('email').send_keys(infile[0])
    time.sleep(.5)
    driver.find_element_by_id('pass').send_keys(infile[1])
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[name="login"]')))
    driver.find_element_by_css_selector('button[name="login"]').click()
    time.sleep(7)
    driver.get('https://www.facebook.com/friends/list')
    time.sleep(5)
    element = driver.find_element_by_css_selector('div[aria-label="All Friends"][role="navigation"] .q5bimw55.rpm2j7zs.k7i0oixp.gvuykj2m.j83agx80.cbu4d94t.ni8dbmo4.eg9m0zos.l9j0dhe7.du4w35lb.ofs802cu.pohlnb88.dkue75c7.mb9wzai9.d8ncny3e.buofh1pr.g5gj957u.tgvbjcpo.l56l04vs.r57mb794.kh7kg01d.c3g1iek1.k4xni2cv')
    # element = driver.find_element_by_css_selector('div[aria-label="All Friends"][role="navigation"] div div:nth-child(2)')
    i = 0
    # totalfriends = int(driver.find_element_by_css_selector('div[aria-label="All Friends"][role="navigation"] .q5bimw55.rpm2j7zs.k7i0oixp.gvuykj2m.j83agx80.cbu4d94t.ni8dbmo4.eg9m0zos.l9j0dhe7.du4w35lb.ofs802cu.pohlnb88.dkue75c7.mb9wzai9.d8ncny3e.buofh1pr.g5gj957u.tgvbjcpo.l56l04vs.r57mb794.kh7kg01d.c3g1iek1.k4xni2cv h2').text.split()[0])
    # start = time.time()
    initiallength = len(driver.find_elements_by_css_selector('div[data-visualcompletion="ignore-dynamic"] a[role="link"]'))
    while True:
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', element)
        # end = time.time()
        time.sleep(5)
        newlenght = len(driver.find_elements_by_css_selector('div[data-visualcompletion="ignore-dynamic"] a[role="link"]'))
        if newlenght == initiallength:
            break
        else:
            initiallength = newlenght
    for res in driver.find_elements_by_css_selector('div[aria-label="All Friends"][role="navigation"] div[data-visualcompletion="ignore-dynamic"] a[role="link"]'):
        link = res.get_attribute('href').split('/')[3]
        if '.php' not in link:
            link.encode('utf-8')
            try:
                file.write(link+'\n')
            except:
                pass
        else:
            name = res.find_element_by_css_selector('span span span').text
            name.encode('utf-8')
            try:
                file.write(name+'\n')
            except:
                pass
    driver.quit()
