import requests
import json
import scrapy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from seleniumwire import webdriver


def main():
    options = {"disable_encoding": True}

    driver = webdriver.Chrome(seleniumwire_options=options)
    driver.maximize_window()
    driver.get('https://twitter.com/')
    time.sleep(2)

    driver.find_element(By.CSS_SELECTOR, 'div.css-901oao.r-1awozwy.r-1cvl2hr.r-6koalj.r-18u37iz').click()
    time.sleep(3)

    inputEmail = driver.find_element(By.CSS_SELECTOR, 'input.r-30o5oe.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf')
    time.sleep(2)
    inputEmail.send_keys('rixtysoft01@gmx.com')
    time.sleep(2)
    inputEmail.send_keys(Keys.ENTER)
    try:
        inputuser = driver.find_element(By.CSS_SELECTOR, 'input.r-30o5oe.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf')
        time.sleep(2)
        inputuser.send_keys('samiyaahmad16')
        time.sleep(2)
        inputuser.send_keys(Keys.ENTER)
    except:
        pass

    inputPass = driver.find_elements(By.CSS_SELECTOR, 'input.r-30o5oe.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf')[-1]
    time.sleep(2)
    inputPass.send_keys('qwerty1234uiop')
    time.sleep(3)
    inputPass.send_keys(Keys.ENTER)
    time.sleep(3)

    searchWord = driver.find_element(By.CSS_SELECTOR, 'input.r-30o5oe.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf')
    time.sleep(2)
    searchWord.send_keys('crypto')
    time.sleep(2)
    searchWord.send_keys(Keys.ENTER)

    # headers = {
    #     "authority": "twitter.com",
    #     "accept": "*/*",
    #     "accept-language": "en-US,en;q=0.9",
    #     "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
    #     "referer": "https://twitter.com/search?q=crypto&src=recent_search_click",
    #     "sec-ch-ua": "\"Chromium\";v=\"104\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"104\"",
    #     "sec-ch-ua-mobile": "?0",
    #     "sec-ch-ua-platform": "\"Windows\"",
    #     "sec-fetch-dest": "empty",
    #     "sec-fetch-mode": "cors",
    #     "sec-fetch-site": "same-origin",
    #     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36",
    #     "x-csrf-token": "314d5c56ca57044c95c0ed4d1885095bec80588e7fac204abb9b5aae003cf2424a8f6cfda28f2d0f466621652dd664f006ebcc2a38f4cbbf2a11159fe808fef92bbf548c29958124a9cb6db2eec0025b",
    #     "x-twitter-active-user": "yes",
    #     "x-twitter-auth-type": "OAuth2Session",
    #     "x-twitter-client-language": "en"
    # }
    # cookies = {
    #     "guest_id_marketing": "v1%3A166072242312942711",
    #     "guest_id_ads": "v1%3A166072242312942711",
    #     "personalization_id": "\"v1_n8VrXJqSotHA5RWR0aCoCQ==\"",
    #     "guest_id": "v1%3A166072242312942711",
    #     "gt": "1559809044688343040",
    #     "_ga": "GA1.2.599921204.1660722434",
    #     "_gid": "GA1.2.971326019.1660722434",
    #     "_sl": "1",
    #     "_twitter_sess": "BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCGyEyKqCAToMY3NyZl9p%250AZCIlNzdkMTlhZjQ3M2YyN2Q0Y2VjOGQ5MDIzYjZlMDE1ZGM6B2lkIiU0YmYw%250AMTBkMGE4YWNkMWZmYTczNzFjN2I0NTQ2YjAwOQ%253D%253D--32888959b6cefc72ee0b3c07de8e6188c2752341",
    #     "kdt": "znKLtMjfoyqg1vkb8JqEXcGUfAu4aHIH7zAcEInj",
    #     "auth_token": "5abbd9eab3648d822dd1a558656951a8190efbbb",
    #     "ct0": "314d5c56ca57044c95c0ed4d1885095bec80588e7fac204abb9b5aae003cf2424a8f6cfda28f2d0f466621652dd664f006ebcc2a38f4cbbf2a11159fe808fef92bbf548c29958124a9cb6db2eec0025b",
    #     "twid": "u%3D1559790688874684416",
    #     "att": "1-Y3nsIc6uSfv3V5iPnbRX9oqLjkWSb3KDDg6Z6BpI",
    #     "lang": "en"
    #
    # page = json.loads(requests.get('https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&include_ext_has_nft_avatar=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_ext_collab_control=true&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&include_ext_sensitive_media_warning=true&include_ext_trusted_friends_metadata=true&send_error_codes=true&simple_quoted_tweet=true&q=crypto&count=100&query_source=recent_search_click&pc=1&spelling_corrections=1&include_ext_edit_control=true&ext=mediaStats%2ChighlightedLabel%2ChasNftAvatar%2CvoiceInfo%2Cenrichments%2CsuperFollowMetadata%2CunmentionInfo%2CeditControl%2Ccollab_control%2Cvibe',headers=headers, cookies=cookies).text)

    resp = [v for v in driver.requests if'adaptive.json' in v.url][0]
    body = json.loads(resp.response.body.decode())

    for link in (list(body['globalObjects']['users'].values())):
        tweeturl = link['screen_name']
        tweet_resp = requests.get(f'https://twitter.com/{tweeturl}')
        tweet_data = scrapy.Selector(text=tweet_resp.text)


if __name__ == "__main__":
    main()
