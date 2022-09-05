import docx
import win32com.client



def create_reply(email:object):
    #open document contating automated reply we need to send
    try:
        doc = docx.Document('Auto response for Facebook Marketplace.docx')
        data = ''
        fullText = []
        for para in doc.paragraphs:
            fullText.append(para.text)
        data = '\r'.join(fullText)
    except IOError:
        print('error opening file')
        exit()
    #make object for replying
    reply = email.Reply()
    #set body of the reply
    # body = data
    reply.HTMLBody = data + reply.HTMLBody
    #hit send
    reply.Send()


if __name__ == '__main__':
    #open file contaning subject line that we need to filter our inbox with
    subjectfile = open('outlookSubjectTofilter.txt','r',encoding='utf-8')
    Subjectline = subjectfile.read().split('\n') #subject line

    outlook = win32com.client.Dispatch('outlook.application') #access outlook application on windows
    mapi = outlook.GetNamespace("MAPI") #get access to all folder in outlook application

    #loop over all accounts currently logged in on outlook in windows
    for account in mapi.Accounts:
        #access inbox of the account
        try:
            inbox = mapi.Folders[account.DeliveryStore.DisplayName].Folders["Inbox"]
        except:
            inbox = mapi.Folders[account.DisplayName].Folders["Inbox"]
        # loop over all emails containg subjectline
        for subject in Subjectline:
            sub = subject.strip().casefold()
            Mails = list(inbox.Items.Restrict("@SQL=""http://schemas.microsoft.com/mapi/proptag/0x0037001f"f" like '%{sub}%'"))
            for mail in Mails:
                if mail.Unread: #check if mail is unread
                    create_reply(mail) # send reply if mail is unread
                    mail.Unread = False # set mail as read.