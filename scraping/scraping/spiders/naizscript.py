import time
from multiprocessing import Process
from selenium import webdriver
from selenium.webdriver.common.by import By

def seleniumfunction(url):
    driver = webdriver.Chrome(executable_path='C:\\Users\\usama\\Downloads\\chromedriver_win32\\chromedriver.exe')
    driver.get(url)

    scroll_pause_time = 3
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        images = driver.find_elements(By.CSS_SELECTOR, 'div.isv-r.PNCib.MSM1fd.BUooTd a')
        for img in images:
            link = img.get_attribute('href')
            try:
                with open('a.txt', 'a', encoding='utf-8') as file:
                    file.write(link + '\n')
            except:
                pass
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    driver.quit()




if __name__ == '__main__':
    queries = ['https://www.google.com/search?q=us+alabama+visa&client=ms-android-samsung-rev2&source=android-home&tbm=isch&sxsrf=ALiCzsYBUyCevV2t06dBbIA3G-hcNLSxtw%3A1671091274478&source=hp&ei=StSaY9LHGoiulwTj56PwBQ&oq=us+alabama+visa&gs_lcp=ChJtb2JpbGUtZ3dzLXdpei1pbWcQAzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJ1DzCFi6fWCvf2gBcAB4AIABAIgBAJIBAJgBAKABAbABBQ&sclient=mobile-gws-wiz-img',
               'https://www.google.com/search?q=us+alabama+visa&tbm=isch&chips=q:us+alabama+visa,online_chips:schengen+visa:RUXEv2oLGns%3D&client=ms-android-samsung-rev2&hl=en&sa=X&ved=2ahUKEwiN9LS1svv7AhWGQaQEHYdAD4MQ4lYoB3oECAEQMw&biw=1903&bih=863',
               'https://www.google.com/search?q=us+alabama+visa&tbm=isch&hl=en&chips=q:us+alabama+visa,online_chips:italy:zxQGKltjzdk%3D&client=ms-android-samsung-rev2&sa=X&ved=2ahUKEwi90KXysvv7AhW4WaQEHem_A6EQ4VYoAHoECAEQJQ&biw=1903&bih=880',
               'https://www.google.com/search?q=us+alabama+visa&tbm=isch&chips=q:us+alabama+visa,online_chips:card:NJWxDr2AZGQ%3D&client=ms-android-samsung-rev2&hl=en&sa=X&ved=2ahUKEwiN9LS1svv7AhWGQaQEHYdAD4MQ4lYoA3oECAEQKw&biw=1903&bih=863',
               'https://www.google.com/search?q=us+alabama+visa&tbm=isch&chips=q:us+alabama+visa,online_chips:germany+visa:4xxVv8ANQJQ%3D&client=ms-android-samsung-rev2&hl=en&sa=X&ved=2ahUKEwiN9LS1svv7AhWGQaQEHYdAD4MQ4lYoBXoECAEQLw&biw=1903&bih=863']
    procs = []

    # instantiating process with arguments
    for query in queries:
        # print(name)
        proc = Process(target=seleniumfunction, args=(query,))
        procs.append(proc)
        proc.start()

    # complete the processes
    for proc in procs:
        proc.join()