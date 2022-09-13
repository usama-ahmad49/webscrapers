import os

import pdfplumber
import win32com.client
from docx2pdf import convert
from datetime import date

def create_reply(email: object):
    # open document contating automated reply we need to send
    try:
        cwd = os.getcwd()
        convert("Auto response for Facebook Marketplace.docx", cwd + '\\'"Auto response for Facebook Marketplace.pdf")
    except:
        pass
    try:
        with pdfplumber.open("Auto response for Facebook Marketplace.pdf") as pdf:
            text = pdf.pages[0]
            Bold_text = text.filter(
                lambda obj: (obj["object_type"] == "char" and "Bold" in obj["fontname"])).extract_text().split('\n')

        textpart = text.extract_text()
        for BT in Bold_text:
            textpart = textpart.split(BT)[0] + '<b>' + BT.strip() + '</b> ' + textpart.split(BT)[1]

        data = textpart.replace('\n', '<br>')
    except IOError:
        print('error opening file')
        exit()
    # make object for replying
    reply = email.Reply()
    # set body of the reply
    # body = data
    # reply.HTMLBody = data + reply.HTMLBody
    reply.HTMLBody = data + reply.HTMLBody
    # hit send
    reply.Send()
    replySentList.append(mail.Sender.Address)


if __name__ == '__main__':
    # open file contaning subject line that we need to filter our inbox with
    subjectfile = open('outlookSubjectTofilter.txt', 'r', encoding='utf-8')
    Subjectline = subjectfile.read().split('\n')  # subject line

    outlook = win32com.client.Dispatch('outlook.application')  # access outlook application on windows
    mapi = outlook.GetNamespace("MAPI")  # get access to all folder in outlook application
    replySentList = []
    # loop over all accounts currently logged in on outlook in windows
    for account in mapi.Accounts:
        # access inbox of the account
        try:
            inbox = mapi.Folders[account.DeliveryStore.DisplayName].Folders["Inbox"]
        except:
            inbox = mapi.Folders[account.DisplayName].Folders["Inbox"]
        # loop over all emails containg subjectline
        for subject in Subjectline:
            sub = subject.strip().casefold()
            Mails = list(
                inbox.Items.Restrict("@SQL=""http://schemas.microsoft.com/mapi/proptag/0x0037001f"f" like '%{sub}%'"))
            for mail in Mails:
                if mail.Unread:  # check if mail is unread
                    create_reply(mail)  # send reply if mail is unread
                    mail.delete()  # set mail as read.
    today = date.today()
    mail = outlook.CreateItem(0)
    mail.To = 'contact@company.com'
    mail.Subject = f"Today's Report: {today}"
    mail.HTMLBody = f"<b>Today's Report Date: {today}<b><br><br><br>{'<br>'.join(replySentList)}<br>"
    mail.Send()