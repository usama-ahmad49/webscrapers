import win32com.client

outlook = win32com.client.Dispatch('outlook.application')
mapi = outlook.GetNamespace("MAPI")

inbox = mapi.GetDefaultFolder(6)

def create_reply(email:object):
    reply = email.Reply()
    body = "Body Text"
    reply.HTMLBody = body + reply.HTMLBody
    reply.Send()

for mail in list(inbox.Items):
    if mail.Unread:
        create_reply(mail)
        mail.Unread = False
