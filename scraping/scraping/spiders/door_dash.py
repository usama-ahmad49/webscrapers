from selenium.webdriver import DesiredCapabilities
from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
import time
import scrapy
import csv

# PROXY = "localhost"
# PORT = 8080
# com.google.gson.JsonObject json = new com.google.gson.JsonObject()
# json.addProperty("proxyType", "MANUAL")
# json.addProperty("httpProxy", PROXY)
# json.addProperty("httpProxyPort", PORT)
# json.addProperty("sslProxy", PROXY)
# json.addProperty("sslProxyPort", PORT)
# DesiredCapabilities cap = new DesiredCapabilities()
# cap.setCapability("proxy", json)
# GeckoDriverService service =new GeckoDriverService.Builder(firefoxBinary).usingDriverExecutable(new File("path to geckodriver")).usingAnyFreePort().usingAnyFreePort().build()
# service.start()
# // GeckoDriver currently needs the Proxy set in RequiredCapabilities
# driver = new FirefoxDriver(service, cap, cap)



header={'Name_resturent','url_resturent','name_product','disc_product','price_product','additions to product',}
wfile=open('doordash.csv', 'w', newline='',encoding='utf-8')
writer=csv.DictWriter(wfile,fieldnames=header)
writer.writeheader()
def get_chrome_capabilities():
    chrome_capabilities = webdriver.DesiredCapabilities.CHROME
    chrome_capabilities['marionette'] = True
    chrome_capabilities['proxy'] = {
        "proxyType": "MANUAL",
        "httpProxy": '85.10.219.97:1080', #'204.12.238.2:19020',
        "ftpProxy": '85.10.219.97:1080', #'204.12.238.2:19020',
        "sslProxy": '85.10.219.97:1080' #'204.12.238.2:19020'
    }
    return chrome_capabilities


def get_firefox_capabilities():
    firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
    firefox_capabilities['marionette'] = True
    firefox_capabilities['proxy'] = {
        "proxyType": "MANUAL",
        "httpProxy": '209.190.32.28:3128', #'204.12.238.2:19020',
        "ftpProxy": '209.190.32.28:3128', #'204.12.238.2:19020',
        "sslProxy": '209.190.32.28:3128' #'204.12.238.2:19020'
    }
    # firefox_capabilities['Disable-infobars']=True
    # firefox_capabilities['start-maximized']=True


if __name__ == '__main__':
    firefox_capabilities = get_firefox_capabilities()
    chrom_c = get_chrome_capabilities()
    # driver = webdriver.Chrome(desired_capabilities=chrom_c)
    driver = webdriver.Firefox()
    driver.maximize_window()
    # driver.get('https://ipleak.net/')
    driver.get('https://www.doordash.com/en-US')
    # time.sleep(5)
    driver.find_element_by_class_name('sc-kIXKos.kxvosg').send_keys('Santa Cruz CA USA')
    print('about to go')
    time.sleep(15)
    print('gone')
    driver.find_element_by_class_name('sc-kIXKos.kxvosg').send_keys(Keys.RETURN)
    driver.find_element_by_class_name('sc-faQXZc.cDXvrt').click()
    # driver.get('https://www.doordash.com/en-US')
    resp_page = scrapy.Selector(text=driver.page_source)
    resturents=resp_page.css('.sc-kFLxrv.iqBnwZ')
    for resturent in resturents:
        item=dict()
        item['Name_resturent']=resturent.css('.sc-fAfrNB.gkWcDe span::text').extract_first()
        url_resturent='https://www.doordash.com{}'.format(resturent.css('a ::attr(href)').extract_first())
        item['url_resturent']=url_resturent
        driver.get(url_resturent)
        time.sleep(5)
        menu_resp_page=scrapy.Selector(text=driver.page_source)
        main_menu=menu_resp_page.css('.sc-GLkNx.diPBzI')
        for ItemPerMainMenu in main_menu:
            itemInSubMenu=ItemPerMainMenu.css('div[data-anchor-id="MenuItem"]')
            for prod in itemInSubMenu:
                item['name_product']=prod.css('.sc-bdVaJa.gImhEG ::text').extract_first().replace('\'','')
                item['disc_product']=prod.css('.sc-gOhbcK.hcdnTW.sc-bdVaJa.huydyu ::text').extract_first()
                item['price_product']=prod.css('.sc-bdVaJa.eEdxFA ::text').extract_first()
                item['additions to product']=', '.join(menu_resp_page.css('.sc-iwsKbI.huuuqa .sc-kNBZmU.fPMlBc span['
                                                                          'class="sc-bdVaJa boGTim"] '
                                                                          '::text').extract() + menu_resp_page.css(
                    '.sc-iwsKbI.huuuqa .sc-kNBZmU.fPMlBc span[class="sc-bdVaJa kHghik"] ::text').extract())


                writer.writerow(item)
                wfile.flush()


