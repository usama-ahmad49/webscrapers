import random
import re
import time

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.firefox.options import Options as ff_options
from scraping import settings


class JSMiddlewareFirefox(object):
    """
    this middleware is used to open multiple(default 20) windows of selenium driver
    """
    display = None
    driver = None
    banded = ['Bot or Not?', 'Access Denied']

    @classmethod
    def from_crawler(cls, crawler):
        """
        This methods binds JSMiddlewareTest.spider_opened and JSMiddlewareTest.spider_closed with spider's
        spider_open and spider_closed methods
        """
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signals.spider_opened)
        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)
        return middleware

    def set_proxy(self, driver, user_agent, http_addr='', http_port=0):
        """
        This function will update proxy in running window of firefox selenium driver

        :param driver: Object of running window driver
        :param http_addr: ip address of proxy
        :param http_port: port of the proxy
        :return:
        """
        driver.execute("SET_CONTEXT", {"context": "chrome"})
        try:
            driver.execute_script("""
              Services.prefs.setIntPref('network.proxy.type', 1);
              Services.prefs.setCharPref("network.proxy.http", arguments[0]);
              Services.prefs.setIntPref("network.proxy.http_port", arguments[1]);
              Services.prefs.setCharPref("network.proxy.ssl", arguments[0]);
              Services.prefs.setIntPref("network.proxy.ssl_port", arguments[1]);
              Services.prefs.setCharPref('network.proxy.socks', arguments[0]);
              Services.prefs.setIntPref('network.proxy.socks_port', arguments[1]);
              Services.prefs.setCharPref('general.useragent.override', arguments[2]);
              """, http_addr, http_port, user_agent)

        finally:
            driver.execute("SET_CONTEXT", {"context": "content"})

    def create_driver(self, spider):
        """
        creates firefox and chrome drivers
        """
        # user_agent = random.choice(spider.user_agents)
        random_proxy = random.choice(spider.proxies) if spider.proxies else None
        options = ff_options()
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-javascript')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--width=1460')
        options.add_argument('--height=780')
        firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
        firefox_capabilities['marionette'] = True
        if random_proxy:  # get a random proxy from spider proxies and set it in driver
            firefox_capabilities['proxy'] = {
                "proxyType": "MANUAL",
                "httpProxy": random_proxy,
                "ftpProxy": random_proxy,
                "sslProxy": random_proxy
            }
        profile = webdriver.FirefoxProfile()
        profile.set_preference("media.peerconnection.enabled", False)
        profile.set_preference("media.navigator.enabled", False)
        # profile.set_preference("general.useragent.override", user_agent)
        profile.update_preferences()

        driver = webdriver.Firefox(executable_path=settings.FIREFOX_WEB_DRIVER_PATH,
                                   capabilities=firefox_capabilities, firefox_profile=profile,
                                   firefox_options=options)
        return driver

    def spider_opened(self, spider):
        """
        :param spider: spider object of running scraper
        """
        if hasattr(spider, 'use_selenium') and getattr(spider, 'use_selenium'):
            self.driver = self.create_driver(spider)

    def spider_closed(self, spider):
        if hasattr(spider, 'use_selenium') and getattr(spider, 'use_selenium'):
            self.close_driver(self.driver)

    def make_request(self, request):
        self.driver.set_page_load_timeout(request.meta.get('timeout', 30))
        self.driver.get(request.url)

    def process_request(self, request, spider):
        """
        Makes selenium request to the URL
        :param request: request that is being processed
        :param spider: spider object of scraper
        :return: HTML response of page scraped using selenium
        """
        if request.meta.get('js'):
            if request.meta.get('proxy'):
                ip, port = spider.get_index(re.findall('(\d+.\d+.\d+.\d+:\d+)', request.meta.get('proxy')), 0).split(
                    ':')
                user_agent = spider.cookies_dict.get(f'{ip}:{port}').get('userAgent')
                self.set_proxy(self.driver, user_agent, ip, port)
            try:
                self.make_request(request)
            except AttributeError as e:
                print('Exception: ', e)
                self.close_driver(self.driver)
                self.driver = self.create_driver(spider)
                self.make_request(request)
            except (TimeoutException, WebDriverException) as e:
                print('Exception: ', e)
                # self.close_driver(self.driver)
                # self.driver = self.create_driver(spider)
                # self.make_request(request)
            time.sleep(10)
            body = self.driver.page_source
            err_items = ['ERR_CONNECTION_TIMED_OUT', 'ERR_PROXY_CONNECTION_FAILED', 'ERR_NO_SUPPORTED_PROXIES',
                         'ERR_TUNNEL_CONNECTION_FAILED', 'recaptcha/api.js', 'recaptcha']
            limit = 0
            """
            If gets one of the err_items in responce body or body length is less than 500,retry url 5 times
            """
            while any([item in body for item in err_items]) and limit < 5 and len(body) < 500:
                self.close_driver(self.driver)
                self.driver = self.create_driver(spider)
                try:
                    self.make_request(request)
                except (TimeoutException, WebDriverException) as e:
                    continue
                body = self.driver.page_source
                limit += 1
            return HtmlResponse(self.driver.current_url, body=body, encoding='utf-8', request=request)

    def close_driver(self, driver):
        try:
            driver.close()
            driver.quit()
        except Exception as e:
            pass
