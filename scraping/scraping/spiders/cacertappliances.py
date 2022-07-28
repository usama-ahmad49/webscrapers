import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

url = 'https://cacertappliances.energy.ca.gov/Pages/Search/AdvancedSearch.aspx'
driver = webdriver.Chrome()
driver.maximize_window()
driver.get(url)
catagorylist = driver.find_elements(By.CSS_SELECTOR, '#ctl00_MainContent_ddlCategories_notificationBorder option')[1:]
for opt in catagorylist:
    driver.find_element(By.CSS_SELECTOR, '#ctl00_MainContent_ddlCategories_notificationBorder').click()
    time.sleep(1)
    opt.click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ctl00_MainContent_ddlApplianceTypes_notificationBorder"))
    )
    ApplianceList = driver.find_elements(By.CSS_SELECTOR, '#ctl00_MainContent_ddlApplianceTypes_notificationBorder option')[1:]
    for opt2 in ApplianceList:
        driver.find_element(By.CSS_SELECTOR, '#ctl00_MainContent_ddlApplianceTypes_notificationBorder').click()
        time.sleep(1)
        opt2.click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ctl00_MainContent_ddlApplianceTypes_notificationBorder"))
        )
        ApplianceStatusList = driver.find_elements(By.CSS_SELECTOR, '#ctl00_MainContent_ddlModelStatus_notificationBorder option')
        for opt3 in ApplianceStatusList:
            driver.find_element(By.CSS_SELECTOR, '#ctl00_MainContent_ddlModelStatus_notificationBorder').click()
            time.sleep(1)
            opt3.click()
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "ctl00_MainContent_chkSelectAll"))
            )
            driver.find_element(By.CSS_SELECTOR, '#ctl00_MainContent_chkSelectAll').click()
