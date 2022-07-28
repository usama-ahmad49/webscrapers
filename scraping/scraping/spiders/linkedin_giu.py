try:
    import pkg_resources.py2_warn
except ImportError:
    pass
import csv
import datetime
import os
import time

import scrapy
from selenium import webdriver
import wx
import wx.lib.agw.hyperlink as hl


class GetData(wx.Dialog):

    def onAddWidget(self, event):
        """"""
        self.number_of_buttons += 1
        label = "Button added"
        name = "button%s" % self.number_of_buttons
        new_button = wx.Button(self, label=label, name=name)
        self.widgetSizer.Add(new_button, 0, wx.ALL, 5)
        # self.frame.fSizer.Layout()
        # self.frame.Fit()

    def __init__(self, parent):
        self.fSizer = wx.BoxSizer(wx.VERTICAL)
        self.number_of_buttons = 0
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "LinkedIn Scraper", size=(650, 400))
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.frame = parent

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        controlSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.widgetSizer = wx.BoxSizer(wx.VERTICAL)

        self.lblemail = wx.StaticText(self.panel, label="Email", pos=(20, 20))
        self.email = wx.TextCtrl(self.panel, value="", pos=(110, 20), size=(500, -1))
        self.lblpass = wx.StaticText(self.panel, label="Password", pos=(20, 60))
        self.password = wx.TextCtrl(self.panel, value="", pos=(110, 60), size=(500, -1), style=wx.TE_PASSWORD)
        self.lblurl = wx.StaticText(self.panel, label="Leads URL", pos=(20, 100))
        self.leadsURL = wx.TextCtrl(self.panel, value="", pos=(110, 100), size=(500, -1))
        self.lblpath = wx.StaticText(self.panel, label="CSV PATH", pos=(20, 140))
        self.csvpath = wx.TextCtrl(self.panel, value="", pos=(110, 140), size=(500, -1))
        self.csvpath.SetHint('leave it blank to save it on Desktop')
        self.lblCSVCount = wx.StaticText(self.panel, label="Multiple CSVs", pos=(20, 180))
        self.multiplecsvs = wx.CheckBox(self.panel,  pos=(110, 180), size=(500, -1))
        self.saveButton = wx.Button(self.panel, label="Start Scraper", pos=(110, 210))
        self.closeButton = wx.Button(self.panel, label="Cancel", pos=(210, 210))
        self.lblHelp = wx.StaticText(self.panel, label="Any Bug or Question please ", pos=(358, 210))
        self.version = wx.StaticText(self.panel, label="Version  2.0", pos=(10, 235))
        self.help = hl.HyperLinkCtrl(self.panel, -1, "Wiki", pos=(592, 235),
                                     URL="https://w.amazon.com/bin/view/AWS/LinkedinScraper")
        self.help = hl.HyperLinkCtrl(self.panel, -1, "Submit a ticket here", pos=(510, 210),
                                     URL="https://phonetool.amazon.com/users/papaianc")

        self.addButton = wx.Button(self.panel, label="Add More", pos=(110, 250))
        self.addButton.Bind(wx.EVT_BUTTON, self.onAddWidget)
        controlSizer.Add(self.addButton, 0, wx.CENTER | wx.ALL, 5)

        self.saveButton.Bind(wx.EVT_BUTTON, self.SaveConnString)
        self.closeButton.Bind(wx.EVT_BUTTON, self.OnQuit)
        self.Bind(wx.EVT_CLOSE, self.OnQuit)
        self.Show()

    def OnQuit(self, event):
        self.result_name = None
        self.Destroy()

    def SaveConnString(self, event):
        self.result_email = self.email.GetValue()
        self.result_password = self.password.GetValue()
        self.result_leads_url = self.leadsURL.GetValue()
        self.result_csv_path = self.csvpath.GetValue()
        self.result_multiple_csv = self.multiplecsvs.GetValue()
        self.Destroy()


def start_scrape(email, linkedIn_password, leads_urls):
    driver = webdriver.Chrome()
    driver.get('https://www.linkedin.com/login')
    time.sleep(5)
    username = driver.find_element_by_name('session_key')
    username.send_keys(email)
    password = driver.find_element_by_name('session_password')
    password.send_keys(linkedIn_password)
    submit = driver.find_element_by_class_name('btn__primary--large.from__button--floating')
    time.sleep(2)
    submit.click()
    while 'feed' not in driver.current_url:
        time.sleep(5)
    # time.sleep(75)
    leads_urls = [lead.strip().split('?')[0] for lead in leads_urls.split(',') if lead.strip()]
    all_items = []
    for listing_url in leads_urls:
        driver.get(listing_url)
        current_page = 1
        time.sleep(5)
        resp = scrapy.Selector(text=driver.page_source)
        total_pages = len(resp.css('.artdeco-pagination__indicator'))
        lead_name = resp.css('.lists-nav__list-name.mr1.inline.t-sans.t-16.t-black.t-bold::text').extract_first('').strip()
        while current_page <= total_pages:
            current_page += 1
            links = resp.css(
                '.t-sans.t-16.t-black.t-bold.lists-detail__view-profile-name-link.ember-view ::attr(href)').extract()
            for link in links:
                link = 'https://www.linkedin.com{}'.format(link)
                driver.get(link)
                time.sleep(2)
                contact_response = scrapy.Selector(text=driver.page_source)
                name = contact_response.css('.profile-topcard-person-entity__name ::text').extract_first(
                    '').strip().split()
                item = dict()
                item['list_name'] = lead_name
                item['ListUrl'] = listing_url
                item['Name'] = name[0]
                item['Surname'] = name[1]
                item['URL'] = link
                item['Role'] = contact_response.css('.profile-position__title ::text').extract_first('').strip()
                item['Company'] = contact_response.css('.profile-position__secondary-title a ::text').extract_first(
                    '').strip()
                for info in contact_response.css('.profile-topcard__contact-info-item'):
                    if info.css('li-icon ::attr(type)').extract_first('') == 'mobile-icon':
                        item['Phone'] = ''.join(info.css('a::text').extract()).strip()
                    if info.css('li-icon ::attr(type)').extract_first('') == 'envelope-icon':
                        item['Email'] = ''.join(info.css('a::text').extract()).strip()
                all_items.append(item)
            next_page_url = '{}?page={}&sortCriteria=CREATED_TIME'.format(listing_url, current_page)
            driver.get(next_page_url)
            resp = scrapy.Selector(text=driver.page_source)
    return all_items


def get_lead_name(items, lead_url):
    for item in items:
        if 'ListUrl' in item.keys() and item['ListUrl'] == lead_url.split('?')[0]:
            return item['list_name']


if __name__ == '__main__':
    now_date = datetime.datetime.now()
    now_date_str = '{}-{}-{}-{}-{}-{}'.format(now_date.year, now_date.month, now_date.day, now_date.hour,
                                              now_date.minute, now_date.second)

    app = wx.App()
    dlg = GetData(parent=None)
    dlg.ShowModal()
    if dlg.result_email:
    # if True:
        email = dlg.result_email
        password = dlg.result_password
        leads_urls = dlg.result_leads_url
        csv_path = dlg.result_csv_path
        multiple_csvs = dlg.result_multiple_csv
        csv_columns = ['Company', 'Name', 'Surname', 'Role', 'Email', 'Phone', 'URL']
        # csvfile = open('D:\davids_project\scraping\scraping\spiders\linkedin.csv', 'w', newline='', encoding="utf-8")
        items = start_scrape(email, password, leads_urls)
        leads_urls_len = len([lead.strip().split('?')[0] for lead in leads_urls.split(',') if lead.strip()])
        single_csv_name = 'linkedin' if leads_urls_len > 1 else ''
        # start_scrape('Davidlincher@gmail.com', 'pythonscript11', 'https://www.linkedin.com/sales/lists/people')
        csv_path = 'C:{}'.format(os.path.join(os.environ["HOMEPATH"], "Desktop")) if not csv_path else csv_path
        if multiple_csvs:
            leads_urls = [lead.strip() for lead in leads_urls.split(',') if lead.strip()]
            for url in leads_urls:
                lead_name = get_lead_name(items, url)
                csvfile = open('{}\{}-{}.csv'.format(csv_path, lead_name, now_date_str), 'w', newline='',
                               encoding="utf-16")
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for item in items:
                    if 'ListUrl' in item.keys() and item['ListUrl'] == url.split('?')[0]:
                        del item['ListUrl']
                        del item['list_name']
                        writer.writerow(item)
        else:
            csvfile = open('{}\{}-{}.csv'.format(csv_path, single_csv_name if single_csv_name else items[0]['list_name']
                                                 , now_date_str), 'w', newline='', encoding="utf-16")
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for item in items:
                del item['ListUrl']
                del item['list_name']
                writer.writerow(item)

    app.MainLoop()
