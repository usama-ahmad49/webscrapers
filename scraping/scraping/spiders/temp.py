from selenium import webdriver
import time
driver= webdriver.Ie()
driver.get('https://www.uber.com/freight/shipper/instant-freight-quote/')
driver.maximize_window()
# time.sleep(3)
driver.find_elements_by_css_selector('._at._cq._dw._dz._db._gj._jl._e5._gl._ca._cb._cc._cd._cf._gg._ce._bx._by._co._cp._cw._cx._bz._cy')[0].send_keys('10001')
elem = True
while elem:
    time.sleep(0.5)
    try:
        driver.find_element_by_css_selector('._ck._dw').click()
        elem = False
    except:
        time.sleep(0.5)
        elem = True

driver.find_elements_by_css_selector('._at._cq._dw._dz._db._gj._jl._e5._gl._ca._cb._cc._cd._cf._gg._ce._bx._by._co._cp._cw._cx._bz._cy')[1].send_keys('10003')
elem1 = True
while elem1:
    time.sleep(0.5)
    try:
        driver.find_element_by_css_selector('._ck._dw').click()
        elem1 = False
    except:
        time.sleep(0.5)
        elem1 = True

driver.find_element_by_id('bui-7__anchor').click()
driver.find_element_by_id('emailAddress').send_keys('bcs@pucit.edu.pk')
driver.find_element_by_id('bui-10__anchor').click()