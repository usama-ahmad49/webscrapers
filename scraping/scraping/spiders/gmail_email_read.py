import base64
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        user_id = 'me'
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        INBOX = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
        for mssg in INBOX['messages']:
            temp_dict = {}
            m_id = mssg['id']  # get id of individual message
            message = service.users().messages().get(userId=user_id, id=m_id).execute()  # fetch the message using API
            payld = message['payload']  # get payload of the message
            headr = payld['headers']  # get header of the payload

            for one in headr:  # getting the Subject
                if one['name'] == 'Subject':
                    msg_subject = one['value']
                    temp_dict['account'] = msg_subject
                else:
                    pass

            temp_dict['Snippet'] = message['snippet']

            try:
                for part in payld['parts'] :
                    if part['filename']:
                        if 'data' in part['body']:
                            data = part['body']['data']
                        else:
                            att_id = part['body']['attachmentId']
                            att = service.users().messages().attachments().get(userId=user_id, messageId=m_id, id=att_id).execute()
                            data = att['data']
                        file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                        path = r'E:\Project\pricescraperlk\webscrapers\webscrapers\scraping\scraping\spiders\attachment'+'\\'+part['filename']

                        with open(path, 'wb') as f:
                            f.write(file_data)

                # mssg_parts = payld['parts']  # fetching the message parts
                # part_one = mssg_parts[0]  # fetching first element of the part
                # part_body = part_one['body']  # fetching body of the message
                # part_data = part_body['data']  # fetching data from the body
                # clean_one = part_data.replace("-", "+")  # decoding from Base64 to UTF-8
                # clean_one = clean_one.replace("_", "/")  # decoding from Base64 to UTF-8
                # clean_two = base64.b64decode(bytes(clean_one, 'UTF-8'))  # decoding from Base64 to UTF-8
                # soup = BeautifulSoup(clean_two, "lxml")
                # mssg_body = soup.body()
                # mssg_body is a readible form of message body
                # depending on the end user's requirements, it can be further cleaned
                # using regex, beautiful soup, or any other method
                # temp_dict['Message_body'] = mssg_body

            except:
                pass

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()
# import os
#
# # import pdfplumber
# import scrapy
# import win32com.client
# import urllib.request
# # from docx2pdf import convert
# from datetime import date



# def read_email_from_gmail():
#     outputDir = r"E:\Project\pricescraperlk\webscrapers\webscrapers\scraping\scraping\spiders\attachment"
#     outlook = win32com.client.Dispatch('outlook.application')  # access outlook application on windows
#     mapi = outlook.GetNamespace("MAPI")  # get access to all folder in outlook application
#     inbox = mapi.Folders['listingsforfacebook@gmail.com'].Folders["Inbox"]
#     # Mails = list(inbox.Items.Restrict("@SQL=""http://schemas.microsoft.com/mapi/proptag/0x0037001f"f" like '%Check%'"))
#     Mails = list(inbox.Items.Restrict("@SQL=""http://schemas.microsoft.com/mapi/proptag/0x0037001f"f" like '%@gmail.com>%'"))
#     adDetails = []
#     for mail in Mails:
#         try:
#             Subjectline = mail.subject
#             body = mail.htmlbody
#             attac = False
#             imagename = []
#             for attachment in mail.Attachments:
#                 attachment.SaveASFile(os.path.join(outputDir, attachment.FileName))
#                 print(f"attachment {attachment.FileName} saved")
#                 imagename.append(attachment.FileName)
#                 attac = True
#
#
#
#             selector = scrapy.Selector(text=body)
#
#             if attac == False:
#                 for i,image in enumerate(selector.css('div img')[1:]):
#                     imgURL = image.css('::attr(src)').extract_first()
#                     nameimgURl = f'image-{i}'
#                     urllib.request.urlretrieve(imgURL, r"E:\Project\pricescraperlk\webscrapers\webscrapers\scraping\scraping\spiders\attachment\{}.jpg".format(nameimgURl))
#                     imagename.append(nameimgURl)
#
#             item = dict()
#             item['account'] = Subjectline
#             item['image'] = imagename
#             value = ''
#             keyname = ''
#             for i in [v for v in selector.css('div:nth-child(2) ::text').extract()]:
#                 if ":" in i:
#                     keyname = i.split(':')[0].replace('\r\n', '')
#                     value = i.split(':')[-1]
#                 else:
#                     value += i
#                 if keyname != '':
#                     item[keyname] = value
#
#             adDetails.append(item)
#             # mail.delete()
#         except Exception as e:
#             print("error when saving the attachment:" + str(e))
#
#     return adDetails


