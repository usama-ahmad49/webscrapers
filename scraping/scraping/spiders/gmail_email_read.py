import os

# import pdfplumber
import scrapy
import win32com.client
import urllib.request
# from docx2pdf import convert
from datetime import date



def read_email_from_gmail():
    outputDir = r"D:\Work\webscrapers\scraping\scraping\spiders\attachment"
    outlook = win32com.client.Dispatch('outlook.application')  # access outlook application on windows
    mapi = outlook.GetNamespace("MAPI")  # get access to all folder in outlook application
    inbox = mapi.Folders['listingsforfacebook@gmail.com'].Folders["Inbox"]
    # Mails = list(inbox.Items.Restrict("@SQL=""http://schemas.microsoft.com/mapi/proptag/0x0037001f"f" like '%Check%'"))
    Mails = list(inbox.Items.Restrict("@SQL=""http://schemas.microsoft.com/mapi/proptag/0x0037001f"f" like '%@gmail.com>%'"))
    adDetails = []
    for mail in Mails:
        try:
            Subjectline = mail.subject
            body = mail.htmlbody
            attac = False
            imagename = []
            for attachment in mail.Attachments:
                attachment.SaveASFile(os.path.join(outputDir, attachment.FileName))
                print(f"attachment {attachment.FileName} saved")
                imagename.append(attachment.FileName)
                attac = True



            selector = scrapy.Selector(text=body)

            if attac == False:
                for i,image in enumerate(selector.css('div img')[1:]):
                    imgURL = image.css('::attr(src)').extract_first()
                    nameimgURl = f'image-{i}'
                    urllib.request.urlretrieve(imgURL, r"D:\Work\webscrapers\scraping\scraping\spiders\attachment\{}.jpg".format(nameimgURl))
                    imagename.append(nameimgURl)

            item = dict()
            item['account'] = Subjectline
            item['image'] = imagename
            value = ''
            keyname = ''
            for i in [v for v in selector.css('div:nth-child(2) ::text').extract()]:
                if ":" in i:
                    keyname = i.split(':')[0].replace('\r\n', '')
                    value = i.split(':')[-1]
                else:
                    value += i
                if keyname != '':
                    item[keyname] = value

            adDetails.append(item)
            # mail.delete()
        except Exception as e:
            print("error when saving the attachment:" + str(e))

    return adDetails


