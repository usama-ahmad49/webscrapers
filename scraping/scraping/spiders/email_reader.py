import docx
import win32com.client

outlook = win32com.client.Dispatch('outlook.application')
mapi = outlook.GetNamespace("MAPI")

inbox = mapi.GetDefaultFolder(6)


def create_reply(email:object):
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
    reply = email.Reply()
    body = data
    reply.HTMLBody = body + reply.HTMLBody
    reply.Send()

for mail in list(inbox.Items):
    if mail.Unread:
        create_reply(mail)
        mail.Unread = False
