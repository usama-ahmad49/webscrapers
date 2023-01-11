from __future__ import print_function

import base64
import csv
import time
from email.message import EmailMessage

from googleapiclient.errors import HttpError

from Google import Create_Service
from tkinter import *

from tkinter import messagebox
def gmail_send_message(email, prereleased, developer, game):
    """Create and send an email message"""

    # creds = None
    SCOPES = ['https://mail.google.com/']
    CLIENT_FILE = 'client_secret.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'

    service = Create_Service(CLIENT_FILE, API_NAME, API_VERSION, SCOPES)
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
        if prereleased == 'Yes':
            message.set_content(f'''Dear devs at {developer},\n
                                I'd like to help with the development of your game {game}.\n
                                Regards''')
        else:
            message.set_content(f'''Dear devs at {developer},\n
                                            I'd like to help with the development of your game {game}.\n
                                            Regards''')

        message['To'] = email
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
    csvfile = open('steamStore.csv', 'r', encoding='utf-8')
    reader = csv.DictReader(csvfile)
    for row in reader:
        if '*' in row['developers']:
            top = Tk()
            top.geometry("100x100")
            top.wm_withdraw()
            messagebox.showwarning("warning", "more then one developer")
        elif row['email'] == '':
            top = Tk()
            top.geometry("100x100")
            top.wm_withdraw()
            messagebox.showwarning("warning","No email found")
        else:
            gmail_send_message(email=row['email'], prereleased=row['pre-release'], developer=row['developers'],
                           game=row['game_name'])
            time.sleep(600)


if __name__ == '__main__':
    readcsvandschedualemail()
