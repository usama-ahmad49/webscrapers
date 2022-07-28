from selenium import webdriver
import mysql.connector
from mysql.connector import Error


def getLaptopDetail():
    mySQLConnection = mysql.connector.connect(host="127.0.0.1",
                                            password="123456789",
                                            user="root",
                                            database="testfloderschema")

    cursor = mySQLConnection.cursor(buffered=True)
    sql_select_query = """select * from jaapnl"""
    cursor.execute(sql_select_query)
    record = cursor.fetchall()
    return record

def addProperty():
    records=getLaptopDetail()
    for record in records:
        driver.find_element_by_id('menu-posts-estate_property').click()
        driver.find_element_by_class_name('page-title-action').click()
        driver.find_element_by_id('title').send_keys(record[1]) #title
        driver.find_element_by_id('content-html').click()
        driver.find_element_by_id('content').send_keys(record[5]) #description
        driver.find_element_by_id('property_price').send_keys(record[3]) #price
        driver.find_element_by_id('property_lot_size').send_keys(record[7]) #size
        driver.find_element_by_id('property_rooms').send_keys(record[10]) #room
        driver.find_element_by_id('property_bedrooms').send_keys(record[11]) #bedroom
        driver.find_element_by_id('property_bathrooms').send_keys(record[12]) #bathroom
        if record[9]=='A+':
            driver.find_element_by_xpath('//*[@id="energy_class"]/option[2]').click()
        if record[9] == 'A':
            driver.find_element_by_xpath('//*[@id="energy_class"]/option[3]').click()
        if record[9] == 'B':
            driver.find_element_by_xpath('//*[@id="energy_class"]/option[4]').click()
        if record[9] == 'C':
            driver.find_element_by_xpath('//*[@id="energy_class"]/option[5]').click()
        if record[9] == 'D':
            driver.find_element_by_xpath('//*[@id="energy_class"]/option[6]').click()
        if record[9] == 'E':
            driver.find_element_by_xpath('//*[@id="energy_class"]/option[7]').click()
        if record[9] == 'F':
            driver.find_element_by_xpath('//*[@id="energy_class"]/option[8]').click()
        if record[9] == 'G':
            driver.find_element_by_xpath('//*[@id="energy_class"]/option[9]').click()
        if record[9] == 'H':
            driver.find_element_by_xpath('//*[@id="energy_class"]/option[10]').click()

        driver.find_element_by_xpath('//*[@id="new_tabbed_interface"]/div[2]/div/div[1]/div[2]').click() #property media
        driver.find_element_by_id('button_new_image').click()
        driver.find_element_by_id('menu-item-upload').click()
        driver.find_element_by_id('__wp-uploader-id-4').click()

        driver.find_element_by_id('publish').click()
        print('this')

if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get(url='https://realzz.nl/wp-admin/')
    driver.maximize_window()
    driver.find_element_by_id('user_login').send_keys('realzz')
    driver.find_element_by_id('user_pass').send_keys('!Welkom@2021!')
    driver.find_element_by_id('wp-submit').click()
    addProperty()

