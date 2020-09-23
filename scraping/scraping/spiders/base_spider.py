import json
import os
import re
import numpy as np
from time import sleep
from io import StringIO
import logging.config
import warnings
import pandas as pd
from datetime import datetime, date
from random import choice
from selenium import webdriver
from selenium.webdriver import Chrome, Firefox
from sqlalchemy import desc

from selenium.webdriver.chrome.options import Options as ch_options
from selenium.webdriver.firefox.options import Options as ff_options
from boto3 import Session

# import MySQLdb
import scrapy
from scrapy import signals

from scraping import settings
# from scraping.models import scrapers
#
# from scraping.models.scrapers import ScraperStats, UserAgents, ColumnsStats, CookieManager

from abc import abstractmethod


class BaseSpider(scrapy.Spider):
    """
    Every spider in this project inherit this spider, it includes all common variables and methods
    """
    total_items = 0
    set_headers = False
    category = ''
    title = ''
    base_url = ''
    file_name = '{}.{}'.format(datetime.now().strftime("%Y%m%d%H%M%S"), settings.FEED_FORMAT)
    custom_settings = {}
    should_send_email = True
    proxy_file_name = 'proxy.txt'
    user_agents = list()
    cookie_url = None
    cookies_dict = dict()
    use_db_proxy = False
    use_file_proxy = False
    use_selenium = False
    headless = True
    use_redis = False
    max_error_count_allowed = 1000
    filter_mysql_warnings = False
    server_name = None
    proxies = None
    random_proxy = None
    use_splash = False
    proxy_limit = 100
    browser = 'firefox'
    os = 'Windows'
    version = 70
    user = ''
    password = ''

    """ This lua script is being used in RotatingHeadersMiddleware to auto update. """
    proxy_lua_script = """
       function main(splash)
          %s
          splash:set_user_agent('%s')
          %s
          splash:go(splash.args.url)
          assert(splash:wait(%d))
          local entries = splash:history()
          local last_response = entries[#entries].response

          return {
            url = splash:url(),
            headers = last_response.headers,
            http_status = last_response.status,
            cookies = splash:get_cookies(),
            html = splash:html(),
          }
       end 
    """

    proxy_lua_script_copy = """
           function main(splash)
              splash:init_cookies(splash.args.cookies)
              splash:set_user_agent("Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:23.0) Gecko/20100101 Firefox/23.0")
              local host = '%(host)s'
              local port = %(port)s
              local user = '%(user)s'
              local password = '%(password)s'
              splash:on_request(function (request)
                request:set_proxy{host, port, username=user, password=password}
              end)
              splash:go(splash.args.url)
              assert(splash:wait(5))
              local entries = splash:history()
              local last_response = entries[#entries].response

              return {
                url = splash:url(),
                headers = last_response.headers,
                http_status = last_response.status,
                cookies = splash:get_cookies(),
                html = splash:html(),
              }
           end 
        """
    countries = 'US'
    frequency = 1

    def __init__(self, **kwargs):
        """
        configure logger to log scraper's logs
        """
        # logging.config.dictConfig(settings.LOGGING)
        self._logger = logging.getLogger(__file__)
        # configure_logging(self._logger, '{}.log'.format(self.name))
        super().__init__(**kwargs)

    @property
    @abstractmethod
    def name(self):
        pass

    @classmethod
    def update_settings(cls, _settings):
        """
       This function run when spider starts and gets all the setting variables from spider updates in setting files
       :param dict _settings: includes all default settings from scrapy.settings.Settings
       """
        version = 50 if cls.browser == 'firefox' else cls.version
        cls.user_agents = []

        new_settings = {'CLOSESPIDER_ERRORCOUNT': cls.max_error_count_allowed,
                        'USER_AGENTS': cls.user_agents}
        if hasattr(cls, 'frequency'):  # set scraper close spider timeout according to the given frequency
            time_period = int((pd.to_timedelta(cls.frequency, unit='D')).total_seconds())
            new_settings.update({'CLOSESPIDER_TIMEOUT': time_period})
        if hasattr(cls, 'use_db_proxy') and cls.use_db_proxy and not cls.use_splash:
            cls.proxies = []
            cls.proxies = [proxy.ip.replace('http://', '').replace('https://', '') for proxy in list(cls.proxies)]
            cls.proxies = cls.get_proxies()  # get number of proxies mentioned in "proxy_limit" variable
            concurrent_requests = 1
            new_settings.update({
                'DOWNLOADER_MIDDLEWARES': {
                    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
                    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
                    **settings.DOWNLOADER_MIDDLEWARES},
                'ROTATING_PROXY_LIST': cls.proxies,
                'CONCURRENT_REQUESTS': concurrent_requests,
                'CONCURRENT_REQUESTS_PER_IP': 1,  # needs to test if it effects
                'AUTOTHROTTLE_TARGET_CONCURRENCY': concurrent_requests,
                'PROXY_MODE': 0})  # 0 = Every requests have different proxy

        elif hasattr(cls, 'use_file_proxy') and cls.use_file_proxy:
            if isinstance(cls.proxy_file_name, list):
                """ e.g. ['proxy.txt', 'proxy_lime_proxies.txt', 'proxy_dreamproxy.txt'] """
                cls.proxies = cls.get_all_file_proxies()
            else:
                path = os.path.join(settings.dir_path, cls.proxy_file_name)
                with open(path, 'r', encoding='utf-8') as proxy_file:
                    cls.proxies = proxy_file.read().strip().split('\n')
                if cls.proxy_file_name == 'proxy.txt':
                    credetials = cls.get_index(cls.get_index(cls.proxies, 0, '').split('@'), 0, '')
                    cls.user = cls.get_index(credetials.split(':'), 1, '').replace('//', '')
                    cls.password = cls.get_index(credetials.split(':'), 2, '')
                    cls.proxies = list(map(lambda x: cls.get_index(x.split('@'), 1, ''), cls.proxies))
                   # cls.proxies = list(map(lambda x: f'http://{x}', cls.proxies))
            total_requests = 1      # needs to test if it effects
            new_settings.update({
                'DOWNLOADER_MIDDLEWARES': {
                    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
                    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
                    **settings.DOWNLOADER_MIDDLEWARES},
                # 'ROTATING_PROXY_LIST_PATH': os.path.join(settings.dir_path, cls.proxy_file_name),
                'ROTATING_PROXY_LIST': cls.proxies,
                'CONCURRENT_REQUESTS': total_requests,
                'CONCURRENT_REQUESTS_PER_IP': total_requests,
                'AUTOTHROTTLE_TARGET_CONCURRENCY': total_requests,
                'PROXY_MODE': 0})  # 0 = Every requests have different proxy
        if hasattr(cls, 'use_redis') and getattr(cls, 'use_redis') and not settings.DEBUG:
            new_settings.update({
                'SCHEDULER': 'scrapy_redis.scheduler.Scheduler',
                'SCHEDULER_QUEUE_CLASS': 'scrapy_redis.queue.FifoQueue',
                # 'REDIS_URL': 'redis://redis:kemdis+emYcOw;iBGIMP4n7iPev@173.82.120.139',
                'REDIS_URL': 'redis://redis@redis',
                'SCHEDULER_IDLE_BEFORE_CLOSE': 20,
                'DUPEFILTER_CLASS': 'scrapy_redis.dupefilter.RFPDupeFilter'})
        if hasattr(cls, 'custom_settings'):
            new_settings.update(cls.custom_settings)

        _settings.setdict(new_settings, priority='spider')

    @classmethod
    def get_all_file_proxies(cls):
        proxies = []
        for file_name in cls.proxy_file_name:
            path = os.path.join(settings.dir_path, file_name)
            with open(path, 'r', encoding='utf-8') as proxy_file:
                if file_name == 'proxy.txt':
                    proxies += [cls.get_index(proxy.split('@'), 1, '') for proxy in
                                proxy_file.read().strip().split('\n')]
                else:
                    proxies += proxy_file.read().strip().split('\n')
        cls.proxy_file_name = ', '.join(cls.proxy_file_name)
        return proxies

    @classmethod
    def get_proxies(cls):
        """
        :return: return's limited number of proxies from given proxies
        """
        proxies = list()
        for i in range(cls.proxy_limit):
            proxy = cls.proxies.pop(cls.proxies.index(choice(cls.proxies)))
            proxies.append(proxy)
        return proxies

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        """
        This methods binds BaseSpider.spider_opened and BaseSpider.spider_closed with scrapy.spider's
        spider_open and spider_closed methods
        """
        spider = super().from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.open_spider, signal=signals.spider_opened)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    @abstractmethod
    def parse(self, response):
        pass

    def get_proxy_lua_script(self):
        """
        If using splash with proxies, This method set proxies in lua script
        """
        if self.proxies:
            self.random_proxy = choice(self.proxies)
            host = self.get_index(self.random_proxy.replace('http://', '').replace('https://', '').split(':'), 0, '')
            port = self.get_index(self.random_proxy.replace('http://', '').replace('https://', '').split(':'), 1, '')
            credentials = dict(host=host, port=port, password=self.password, user=self.user)
            script_text = self.proxy_lua_script % credentials
            if not self.user or not self.password:
                script_text = script_text.replace("local user = ''", "")
                script_text = script_text.replace("local password = ''", "")
            return script_text

    def get_random_proxy(self):
        """
        return a random_proxy from scraper's proxies
        :return: random proxy
        """
        self.random_proxy = choice(self.proxies)
        return self.random_proxy

    def open_spider(self, spider):
        pass

    def spider_closed(self, spider):
        """
        This method performs all necessary action that need to perform before scraper close
        """
        pass

    @classmethod
    def get_index(cls, lst, index, default=''):
        """
        return element on given index from list
        :param lst: list from which we will return element
        :param index: index of element
        :param default: return value if index out of range
        :return:
        """
        return lst[index] if len(lst) > index else default

    @staticmethod
    def get_dict_value(data, key_list, default=''):
        """
        gets a dictionary and key_list, apply key_list sequentially on dictionary and return value
        :param data: dictionary
        :param key_list: list of key
        :param default: return value if key not found
        :return:
        """
        for key in key_list:
            if data and isinstance(data, dict):
                data = data.get(key, default)
            else:
                return default
        return data

    @staticmethod
    def get_frequency(args):
        """
        gets frequency from commandline arguments
        """
        return int([arg.replace('frequency=', '') for arg in args if 'frequency' in arg][0]) if [
            arg.replace('frequency=', '') for arg in args if 'frequency' in arg] else None

    def clean_timestamp(self, value):
        """
        This method will clean fields which contain date in the format /Date(1533859200000)/
        :param value:
        :return: Datetime object or None
        """
        if not isinstance(value, str):
            return None
        timestamp_string = re.findall('([0-9]+)', value)[0]
        if int(timestamp_string):
            return datetime.fromtimestamp(int(timestamp_string) / 1000)
        else:
            return None

    @staticmethod
    def get_hours_minutes(time_delta):
        """
        Given a time delta object it will return minutes and seconds
        :param time_delta: timedelta object
        :return: hours minutes seconds
        """
        total_seconds = time_delta.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        if hours:
            return '{} Hour(s) {} minute(s) {} second(s)'.format(hours, minutes, seconds)
        else:
            return '{} minute(s) {} second(s)'.format(minutes, seconds)

    @classmethod
    def create_driver(cls, random_proxy, user_agent, for_headers=False, webrtc=True):
        """
        creates firefox or chrome driver with given settings
        :param random_proxy:
        :param user_agent:
        :param for_headers:
        :param webrtc:
        :return:
        """
        if cls.browser == 'firefox':
            options = ff_options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-javascript')
            options.add_argument('--disable-dev-shm-usage')
            firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
            firefox_capabilities['marionette'] = True
            if random_proxy:
                firefox_capabilities['proxy'] = {
                    "proxyType": "MANUAL",
                    "httpProxy": random_proxy,
                    "ftpProxy": random_proxy,
                    "sslProxy": random_proxy
                }
            profile = webdriver.FirefoxProfile()
            profile.set_preference("media.peerconnection.enabled", False)
            profile.set_preference("media.navigator.enabled", False)
            profile.set_preference("general.useragent.override", user_agent)
            profile.update_preferences()

            if for_headers:
                driver = Firefox(executable_path=settings.FIREFOX_WEB_DRIVER_PATH, capabilities=firefox_capabilities,
                                 firefox_profile=profile, firefox_options=options)
            else:
                driver = webdriver.Firefox(executable_path=settings.FIREFOX_WEB_DRIVER_PATH,
                                           capabilities=firefox_capabilities,
                                           firefox_profile=profile, firefox_options=options)
        else:
            options = ch_options()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-javascript')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument(f'user-agent={user_agent}')
            if random_proxy:
                options.add_argument(f'--proxy-server={random_proxy}')

            if webrtc:
                # options.add_extension(settings.WEB_DRIVER_EXTENSION_PATH)
                pass
            else:
                options.add_argument('--headless')

            if for_headers:
                driver = Chrome(settings.WEB_DRIVER_PATH, chrome_options=options)
            else:
                driver = webdriver.Chrome(settings.WEB_DRIVER_PATH, chrome_options=options)

        return driver

    @classmethod
    def close_driver(cls, driver):
        try:
            driver.close()
            driver.quit()
        except Exception as e:
            pass
