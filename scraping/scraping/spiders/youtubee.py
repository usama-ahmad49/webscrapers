from selenium import webdriver
import time
import scrapy
import csv
from datetime import datetime
from selenium.webdriver.firefox.options import Options


from csv import DictWriter

new = []

csv_columns = ['channel', 'Channel Link', 'subscribers', 'Publish Date', 'Country', 'Subscriber Growth Last Month',
               'Views Growth Last Month', 'Total Views', 'Videos', 'Last Upload Date', 'Category', 'Last Video Id',
               'Last Video Title', 'Description', 'Keywords', 'Last Updated', "Has Email"]
csvfile = open('youtube.csv', 'w', newline='', encoding="utf-8")
writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
writer.writeheader()

if __name__ == '__main__':
    count = 1
    f = open("youtube_input.txt", "r")
    state_input = f.read()
    options = Options()
    options.headless = True
    driver = webdriver.Chrome()

    for i in state_input.split("\n"):
        if i == "":
            break
        driver.get(i)
        time.sleep(6)
        # delay = 5
        # try:
        #     myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'VfPpkd-RLmnJb')))
        #     driver.find_element_by_css_selector("div.VfPpkd-RLmnJb").click()
        #     print("Page is ready!")
        # except TimeoutException:
        #     print("Loading took too much time!")
        try:
            driver.find_element_by_css_selector("div.VfPpkd-RLmnJb").click()
            time.sleep(6)
        except:
            pass

        driver.find_element_by_xpath("//*[@id='tabsContent']/tp-yt-paper-tab[6]").click()
        time.sleep(8)
        response = scrapy.Selector(text=driver.page_source)
        channel = response.css("ytd-channel-name#channel-name yt-formatted-string.style-scope.ytd-channel-name::text").get()
        driver.add_cookie({'name': 'ST-eyu0eb',
                           'value': 'itct=CB0Q8JMBGAUiEwiho7n4rJ7wAhUS5FUKHSc2DXI%3D&csn=MC4wMTgwOTgwMzUyNTY1ODAyNw..&endpoint=%7B%22clickTrackingParams%22%3A%22CB0Q8JMBGAUiEwiho7n4rJ7wAhUS5FUKHSc2DXI%3D%22%2C%22commandMetadata%22%3A%7B%22webCommandMetadata%22%3A%7B%22url%22%3A%22%2Fc%2FCrazyFrogOfficial%2Fabout%22%2C%22webPageType%22%3A%22WEB_PAGE_TYPE_CHANNEL%22%2C%22rootVe%22%3A3611%2C%22apiUrl%22%3A%22%2Fyoutubei%2Fv1%2Fbrowse%22%7D%7D%2C%22browseEndpoint%22%3A%7B%22browseId%22%3A%22UC4XR0EZ0oHwSV2XhhShzX5A%22%2C%22params%22%3A%22EgVhYm91dA%253D%253D%22%2C%22canonicalBaseUrl%22%3A%22%2Fc%2FCrazyFrogOfficial%22%7D%7D'})

        subscribers = response.css("yt-formatted-string#subscriber-count::text").get().split()[0]
        joined_date = response.xpath(
            "/html/body/ytd-app/div/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-channel-about-metadata-renderer/div[2]/yt-formatted-string[2]/span[2]/text()").get()
        country = response.xpath("//*[@id='details-container']/table/tbody/tr[2]/td[2]/yt-formatted-string/text()").get()
        total_views = response.xpath("//*[@id='right-column']/yt-formatted-string[3]/text()").get().split()[0]
        if country is None:
            country = ""
        if response.css("a.yt-simple-endpoint.style-scope.yt-formatted-string::text").get() == 'Sign in':
            email = "Yes"
        else:
            email = "No"
        driver.find_element_by_xpath(
            "/html/body/ytd-app/div/ytd-page-manager/ytd-browse/div[3]/ytd-c4-tabbed-header-renderer/tp-yt-app-header-layout/div/tp-yt-app-header/div[2]/tp-yt-app-toolbar/div/div/tp-yt-paper-tabs/div/div/tp-yt-paper-tab[2]/div").click()
        time.sleep(3)
        ht = driver.execute_script("return document.documentElement.scrollHeight;")
        while True:
            prev_ht = driver.execute_script("return document.documentElement.scrollHeight;")
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(5)
            ht = driver.execute_script("return document.documentElement.scrollHeight;")
            if prev_ht == ht:
                break
        res = scrapy.Selector(text=driver.page_source)

        try:
            with open("youtube_old.csv", 'r', errors='ignore') as file:
                csv_file = csv.DictReader(file)
                for row in csv_file:
                    if row["channel"] == channel:

                        item = dict()
                        item["channel"] = channel
                        item["Channel Link"] = i
                        subs = subscribers
                        if "K" in subs:
                            num = subs.replace("K", "")
                            item["subscribers"] = float(num) * 1000
                        elif "M" in subs:
                            num = subs.replace("M", "")
                            item["subscribers"] = float(num) * 1000000
                        elif "B" in subs:
                            num = subs.replace("B", "")
                            item["subscribers"] = float(num) * 1000000000
                        else:
                            item["subscribers"] = float(subscribers)
                        if "K" in row["subscribers"]:
                            num = row["subscribers"].replace("K", "")
                            row["subscribers"] = float(num) * 1000
                        elif "M" in row["subscribers"]:
                            num = row["subscribers"].replace("M", "")
                            row["subscribers"] = float(num) * 1000000
                        elif "B" in row["subscribers"]:
                            num = row["subscribers"].replace("B", "")
                            row["subscribers"] = float(num) * 1000000000
                        else:
                            row["subscribers"] = row["subscribers"]
                        item["Publish Date"] = joined_date
                        item["Country"] = country
                        item["Subscriber Growth Last Month"] = item["subscribers"] - float(row["subscribers"])
                        item["Total Views"] = total_views
                        item["Views Growth Last Month"] = float(total_views.replace(",", "")) - float(
                            row["Total Views"].replace(",", ""))
                        item["Videos"] = len(res.css("a#thumbnail::attr(href)"))
                        driver.get("https://www.youtube.com" + res.css("a#thumbnail::attr(href)")[0].get())
                        time.sleep(5)
                        resp = scrapy.Selector(text=driver.page_source)
                        item["Last Upload Date"] = resp.css("div#date yt-formatted-string::text").get()
                        item["Category"] = resp.xpath("//meta[@itemprop='genre']/@content").get()
                        item["Last Video Id"] = resp.xpath("//meta[@itemprop='videoId']/@content").get()
                        last_video = resp.css("h1.title yt-formatted-string::text").get()
                        if last_video is None:
                            last_video = resp.css("h1.title yt-formatted-string span::text")[0].get() + resp.css(
                                "h1.title yt-formatted-string a::text").get() + \
                                         resp.css("h1.title yt-formatted-string span::text")[2].get()
                        item["Last Video Title"] = last_video
                        item["Last Video Title"] = resp.css("h1.title yt-formatted-string::text").get()
                        item["Description"] = resp.xpath("//meta[@itemprop='description']/@content").get()
                        item["Keywords"] = resp.xpath("//meta[@name='keywords']/@content").get()
                        item["Last Updated"] = datetime.now()
                        item["Has Email"] = email
                        writer.writerow(item)
                        csvfile.flush()
                    else:
                        with open("youtube_old.csv", 'r', errors='ignore') as fi:
                            csv_fi = csv.DictReader(fi)
                            for rows in csv_fi:
                                for k, v in rows.items():
                                    if "channel" in k:
                                        if v == "":
                                            continue
                                        else:
                                            new.append(v)
                        if channel in new:
                            pass
                        else:
                            out_file = open("youtube_old.csv", "a", errors='ignore', newline='')
                            dictwriter_object = DictWriter(out_file, fieldnames=csv_columns)
                            items = dict()
                            items["channel"] = channel
                            items["Channel Link"] = i
                            subs = subscribers
                            if "K" in subs:
                                num = subs.replace("K", "")
                                items["subscribers"] = float(num) * 1000
                            elif "M" in subs:
                                num = subs.replace("M", "")
                                items["subscribers"] = float(num) * 1000000
                            elif "B" in subs:
                                num = subs.replace("B", "")
                                items["subscribers"] = float(num) * 1000000000
                            else:
                                items["subscribers"] = float(subscribers)
                            items["Publish Date"] = joined_date
                            items["Country"] = country
                            items["Subscriber Growth Last Month"] = 0
                            items["Total Views"] = total_views
                            items["Views Growth Last Month"] = 0
                            items["Videos"] = len(res.css("a#thumbnail::attr(href)"))
                            driver.get("https://www.youtube.com" + res.css("a#thumbnail::attr(href)")[0].get())
                            time.sleep(5)
                            resp = scrapy.Selector(text=driver.page_source)
                            items["Last Upload Date"] = resp.css("div#date yt-formatted-string::text").get()
                            items["Category"] = resp.xpath("//meta[@itemprop='genre']/@content").get()
                            items["Last Video Id"] = resp.xpath("//meta[@itemprop='videoId']/@content").get()
                            last_video = resp.css("h1.title yt-formatted-string::text").get()
                            if last_video is None:
                                last_video = resp.css("h1.title yt-formatted-string span::text")[
                                                     0].get() + resp.css(
                                        "h1.title yt-formatted-string a::text").get() + \
                                                 resp.css("h1.title yt-formatted-string span::text")[2].get()
                                items["Last Video Title"] = last_video

                            items["Last Video Title"] = resp.css("h1.title yt-formatted-string::text").get()
                            items["Description"] = resp.xpath("//meta[@itemprop='description']/@content").get()
                            items["Keywords"] = resp.xpath("//meta[@name='keywords']/@content").get()
                            items["Last Updated"] = datetime.now()
                            items["Has Email"] = email
                            dictwriter_object.writerow(items)
                            del new[:]
                            out_file.close()
        except IOError:
            print("File not accessible")

    driver.close()
