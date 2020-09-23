from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

chrome_options = Options()
chrome_options.add_extension('E:/Project/genratedfiles/amzscout.crx')
driver = webdriver.Chrome(options=chrome_options, executable_path='C:\Windows\chromedriver')


# Readfile=open('AmzshoutProdSearchTerms.csv','r')
# inp=Readfile.read()
driver.get('https://amazon.com')
searchbar=driver.find_element_by_id('twotabsearchtextbox')
searchbar.send_keys('underwear')
time.sleep(5)
searchbar.send_keys(Keys.RETURN)
time.sleep(5)
button=driver.find_element_by_xpath('/html/body/amzscout-pro/os-circle')
button.click()
time.sleep(5)
if(driver.find_element_by_class_name('agmodal__wrapper agmodal__wrapper--level-1 ng-scope agmodal__wrapper--visible')):
    driver.find_element_by_class_name('i-ad-close').click()

time.sleep(7)
totalresults=driver.find_element_by_class_name('totals-item__val ng-binding').get_attribute("innerText")[0]
AvgMonthlySales = driver.find_element_by_class_name('totals-item__val ng-binding').get_attribute("innerText")[1]
AvgMonthlyRevenue = driver.find_element_by_class_name('totals-item__val ng-binding').get_attribute("innerText")[2]
AvgPrice = driver.find_element_by_class_name('totals-item__val ng-binding').get_attribute("innerText")[3]
AvgReviews = driver.find_element_by_class_name('totals-item__val ng-binding').get_attribute("innerText")[4]
driver.find_element_by_id('score-item').click()
nicheScore=driver.find_element_by_class_name('os-progress-circle__score ng-binding').get_attribute('innerText')
profitDetails=driver.find_element_by_class_name('title ng-binding').get_attribute('innerText')[0].join(driver.find_element_by_class_name('description ng-binding').get_attribute('innerText')[0]).join(driver.find_element_by_class_name('title ng-binding').get_attribute('innerText')[1]).join(driver.find_element_by_class_name('description ng-binding').get_attribute('innerText')[1])


print('it worked')

