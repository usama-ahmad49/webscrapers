from __future__ import print_function

import base64
import csv
import os
from email.message import EmailMessage

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from Google import Create_Service

def gmail_send_message():
    """Create and send an email message"""

    # creds = None
    SCOPES = ['https://mail.google.com/']
    CLIENT_FILE = 'client_secret.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'

    service = Create_Service(CLIENT_FILE, API_NAME, API_VERSION,SCOPES)
    # service.users.messages.send('usamaahmed2222@gmail.com')

    # if os.path.exists('token.json'):
    #     creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # # If there are no (valid) credentials available, let the user log in.
    # if not creds or not creds.valid:
    #     if creds and creds.expired and creds.refresh_token:
    #         creds.refresh(Request())
    #     else:
    #         flow = InstalledAppFlow.from_client_secrets_file(
    #             'credentials.json', SCOPES)
    #         creds = flow.run_local_server(port=0)
    #     # Save the credentials for the next run
    #     with open('token.json', 'w') as token:
    #         token.write(creds.to_json())

    try:
        # service = build('gmail', 'v1', credentials=creds)
        message = EmailMessage()

        message.set_content(f'''Dear devs at {developer},\n
                            I'd like to help with the development of your game {game}.\n
                            Regards''')

        message['To'] = 'usamaahmed2222@gmail.com'
        message['From'] = 'rixtysoft01@gmail.com'
        message['Subject'] = 'Automated draft'


        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
            .decode()

        create_message = {
            'raw': encoded_message
        }
        # pylint: disable=E1101
        send_message = (service.users().messages().send
                        (userId="me", body=create_message).execute())
        print(F'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None
    return send_message

def readcsvandschedualemail():
    csvfile = open('steamStore.csv', 'r')
    reader = csv.DictReader(csvfile)
    for row in reader:
        gmail_send_message()

if __name__ == '__main__':
    gmail_send_message()