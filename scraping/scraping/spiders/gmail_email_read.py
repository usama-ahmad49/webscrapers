import os

# import pdfplumber
import win32com.client
# from docx2pdf import convert
from datetime import date

# Define the SCOPES. If modifying it, delete the token.pickle file.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def read_email_from_gmail():
    outputDir = r"C:\attachment"
    outlook = win32com.client.Dispatch('outlook.application')  # access outlook application on windows
    mapi = outlook.GetNamespace("MAPI")  # get access to all folder in outlook application
    inbox = mapi.Folders['listingsforfacebook@gmail.com'].Folders["Inbox"]
    Mails = list(inbox.Items.Restrict("@SQL=""http://schemas.microsoft.com/mapi/proptag/0x0037001f"f" like '%@gmail.com>%'"))
    for mail in Mails:
        try:
            Subjectline = mail.subject
            body = mail.htmlbody
            for attachment in mail.Attachments:
                attachment.SaveASFile(os.path.join(outputDir, attachment.FileName))
                print(f"attachment {attachment.FileName} saved")
        except Exception as e:
            print("error when saving the attachment:" + str(e))




read_email_from_gmail()