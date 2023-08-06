#Import packages. 
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
import pickle
import os
import email
import datetime as dt
from bs4 import BeautifulSoup
import pandas as pd

class Gmail:
    @staticmethod
    def mark_as_read(service, message_id):
        #Modify message label.
        response = service.users().messages().modify(userId="me", id=message_id, body= {
            "removeLabelIds" : ["UNREAD"]
        }).execute()

        return response
    @staticmethod
    def list_messages(service, max_results=1000, labels=None, query=None, read=False):
        #List all the messages. 
        messages = service.users().messages().list(userId="me",labelIds=labels, maxResults=max_results, q=query).execute()
        return messages.get("messages")

    @staticmethod
    def get_attachements(service, message_id, storage_path):
        message = service.users().messages().get(userId="me", id=message_id).execute()
        for part in message['payload']['parts']:
            if part['filename']:

                file_data = base64.urlsafe_b64decode(part['body']['data'].encode('UTF-8'))

                path = ''.join([storage_path, part['filename']])

                f = open(path, 'w')
                f.write(file_data)
                f.close()

    @staticmethod
    def parse_email(service, message_id, content_type):
        #Get the message. 
        message = service.users().messages().get(userId="me", id=message_id, format="raw").execute()

        #Decode the Base64 format.
        raw = message.get("raw")
        mail = email.message_from_bytes(base64.urlsafe_b64decode(raw))

        #Get message details.
        date = mail.get("Date").split("-")[0].strip()
        date = dt.datetime.strptime(date, "%a, %d %b %Y %H:%M:%S")
        from_ = mail.get("From")
        subject = mail.get("Subject")
        to_ = mail.get("To")

        #Loop through each part of the message. 
        body = []
        for part in mail.walk():
            #Get only the plain text. 
            if part.get_content_type()==content_type:
                #Add it to the message. 
                body.append(part.as_string())

        output = {
            "date" : date,
            "from_" : from_,
            "subject" : subject,
            "to_" : to_,
            "body" : body
        }

        return output