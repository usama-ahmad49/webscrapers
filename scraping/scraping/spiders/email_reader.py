import win32com.client

outlook = win32com.client.Dispatch('outlook.application')
mapi = outlook.GetNamespace("MAPI")

inbox = mapi.GetDefaultFolder(6)

def create_reply(email:object):
    reply = email.Reply()
    body = '''Thank you for responding to our ad. The landlord has already received over 30 responses and will probably pick a tenant from those applications. I suggest that you register on the website https://www.homefinders.rentals 

and you will start getting notified with rentals BEFORE we post them here, so you won't miss out on any more great listings!  It is FREE to Register !!

With over 1,100 properties, covering 24 cities across BC, HomeFinders has you covered. You can;
-Search our database (for Free)
-Register (for Free) and be notified when a new rental hits the market that matches what you are looking for.
- Hire us to search through 13 different rental websites every day (so you don't have to).
- Hire us to tip you off on rentals BEFORE they hit the market.

Imagine waking up to a NEW list of rentals every day until you find a place!

Check out this information Video https://youtu.be/7x1x0skLRWs

Proud Member of the Better Business Bureau with an A+ rating for the last 17 years.
https://www.bbb.org/.../renta.../homefinders-0037-2417284...



'''
    reply.HTMLBody = body + reply.HTMLBody
    reply.Send()

for mail in list(inbox.Items):
    if mail.Unread:
        create_reply(mail)
        mail.Unread = False
