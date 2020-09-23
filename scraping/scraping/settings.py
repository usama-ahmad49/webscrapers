# -*- coding: utf-8 -*-

# Scrapy settings for bigdatainsights project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import os
import json

import urllib

file_path = os.path.realpath(__file__)
dir_path, _ = os.path.split(file_path)
LOG_PATH = os.path.join(os.path.abspath(os.path.join(dir_path, '..', '..')), 'logs')
# PROJECT_DIR = dir_path
PROJECT_DIR, _ = os.path.split(dir_path)

if not os.path.isdir(LOG_PATH):
    os.mkdir(LOG_PATH)

with open(os.path.join(dir_path, 'config.json'), 'r') as f:
    config = json.load(f)


BOT_NAME = 'scraping'

SPIDER_MODULES = ['scraping.spiders']
NEWSPIDER_MODULE = 'scraping.spiders'

DEBUG = config['DEBUG']

# Crawl responsibly by identifying yourself (and your website) on the user-agent

USER_AGENTS = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
               'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
               'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
               'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
               'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
               'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
               'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
               'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
               ]

# USER_AGENT = ('Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
#               'Chrome/68.0.3440.106 Safari/537.36')
# USER_AGENT_CHOICES = [
#     'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:23.0) Gecko/20100101 Firefox/23.0',
#     'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36',
#     'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)',
#     'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36',
#     'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36',
#     'Mozilla/5.0 (X11; Linux x86_64; rv:24.0) Gecko/20140205 Firefox/24.0 Iceweasel/24.3.0',
#     'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
#     'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:28.0) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
# ]

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
DB_CREDENTIALS = config['DB_CREDENTIALS']
POSTGRES_DB_CREDENTIALS = config['POSTGRES_DB_CREDENTIALS']
DATABASE_BBI = dict(DB_CREDENTIALS, db='price_data')
DATABASE_BBI['password'] = urllib.parse.quote(DATABASE_BBI['password'])
DATABASE_URI = config['DATABASE_URI']
POSTGRES_DATABASE_URI = config['POSTGRES_DATABASE_URI']
# DATABASE = config['GOOGLE_DATABASE']
# DATABASE_URI = config['GOOGLE_DATABASE_URI']
WEB_DRIVER_PATH = os.path.join(config['WEB_DRIVER']['PATH'], config['WEB_DRIVER']['NAME'])
FIREFOX_WEB_DRIVER_PATH = os.path.join(config['WEB_DRIVER']['PATH'], config['WEB_DRIVER']['FIREFOX_NAME'])
WEB_DRIVER_EXTENSION_PATH = os.path.join(config['WEB_DRIVER_EXTENSION']['PATH'], config['WEB_DRIVER_EXTENSION']['NAME'])
# WEB_DRIVER_PATH_IE = os.path.join(config['WEB_DRIVER']['PATH'], config['WEB_DRIVER']['NAME_IE'])
# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0
RANDOMIZE_DOWNLOAD_DELAY = True
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 1
# CONCURRENT_REQUESTS_PER_IP = 1
# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

# DUPEFILTER_CLASS = 'scrapy.dupefilter.BaseDupeFilter'
# HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}
# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    # 'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
    # 'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 600,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'scraping.middlewares.JSMiddlewareFirefox': 702,

    'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 90,
    'tutorial.randomproxy.RandomProxy': 100,
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
    'tutorial.spiders.rotate_useragent.RotateUserAgentMiddleware' :400,
}
# SPLASH_URL = 'http://localhost:8050'
SPLASH_URL = 'http://0.0.0.0:8050'
# SPLASH_URL = 'http://10.150.0.4:8050'
# SPLASH_URL = 'http://173.82.119.23:8050/'     # Staging server, we use this server to test splash on local
# SPLASH_URL = 'http://192.168.168.62:8050'  # local splash server
RANDOM_UA_PER_PROXY = True
FAKEUSERAGENT_FALLBACK = 'Mozilla'
# DOWNLOAD_HANDLERS = {
#     'http': 'bigdatainsights.dhandler.WebkitDownloadHandler',
#     'https': 'bigdatainsights.dhandler.WebkitDownloadHandler',
# }
# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html

# To save CSV while scraper is running on production, we use feeds (builtin scrapy extension)
FEED_URI = config['FEED_URI']
FEED_FORMAT = 'csv'
FEED_STORAGES = config['FEED_STORAGES']
FILE_PATH = config['FILE_PATH']

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# In local we use CSV pipeline to store data in CSV
if DEBUG:
    ITEM_PIPELINES = {'scraping.pipelines.base.CSVPipeline': 400}
else:
    # On Production we use Feeds to save CSVs
    ITEM_PIPELINES = {}
# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = CONCURRENT_REQUESTS
AUTOTHROTTLE_DEBUG = False

# Retry Middleware Settings
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429, 524]      # If we get this status code in response we will try same link "RETRY_TIMES" times
# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings

HTTPCACHE_ENABLED = config.get('HTTPCACHE_ENABLED', False)
HTTPCACHE_EXPIRATION_SECS = 28800       # expire after 8 hours
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# Email Configuration
MAIL_ADMINS = [('scraping', 'scraping@scraping.pk')]
ADMIN_EMAILS = ['scraping@scraping.pk']

# MAIL_HOST = 'mail.bigdataanalytics.pk'
MAIL_HOST = 'smtp.gmail.com'
MAIL_TO = 'scraping@scraping.pk'  # Mailing list
MAIL_FROM = 'no-reply@scraping.com'  # Mailing list
MAIL_USER = 'no-reply@scraping.com'
MAIL_PASS = 'h5aVyU%r'
MAIL_PORT = 587

SFTP_HOST = config['SFTP']['HOST']
SFTP_USER = config['SFTP']['USER']
SFTP_PASS = config['SFTP']['PASS']
SFTP_BASE_URI = 'sftp://%s:%s@%s' % (SFTP_USER, SFTP_PASS, SFTP_HOST)

GOOGLE_KEY = config.get('GOOGLE_MAPS_KEY', '')
AWS_ACCESS_KEY_ID = config.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = config.get('AWS_SECRET_ACCESS_KEY', '')
AWS_LOG_BUCKET = config.get('AWS_LOGS_BUCKET', '')
AWS_STORAGE_API_RESPONSE_BUCKET_NAME = 'bbi-api-response'
AWS_CSV_BUCKET_NAME = 'bbi-scraped-items'
SLACK_BOT_ACCESS_TOKEN = config.get('SLACK_BOT_ACCESS_TOKEN', '')
