import unittest

import common
import crawl_linkedin
import time
import scrapy



class Test_crawl_linkedin(unittest.TestCase):
    stat_file = crawl_linkedin.STAT_FILE
    # crawled = common.load_crawled('otnzwna.stat')
    # base_url = crawl_linkedin.base_url
    driver = crawl_linkedin.makebrowserandsignin()
    driver.get('https://www.linkedin.com/search/results/people/?currentCompany=%5B%22326376%22%2C%2227165%22%5D&origin=COMPANY_PAGE_CANNED_SEARCH&sid=ey%2C')
    # crawled = common.load_crawled(stat_file)
    Selector = scrapy.Selector(text=driver.page_source)
    sel = Selector.css('.reusable-search__result-container')[0]
    data = crawl_linkedin.parse_profile(sel)


    def test_parse_profile(self):
        for item in self.data:
            self.assertNotEqual(item['name'], "")
            self.assertNotEqual(item['url'], "")
            self.assertNotEqual(item['profession'], "")
            self.assertNotEqual(item['location'], "")


if __name__ == "__main__":
    unittest.main()

