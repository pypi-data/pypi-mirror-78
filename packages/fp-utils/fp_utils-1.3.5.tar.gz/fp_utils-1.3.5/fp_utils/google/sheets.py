from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pandas as pd

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

class Sheets:
    @staticmethod
    def get_google_sheet(spreadsheet_id, sheet_name, range_name):
        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('config/token.pickle'):
            with open('config/token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'config/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('config/token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        SPREADSHEET_ID = spreadsheet_id
        SHEET_NAME = sheet_name + "!" + range_name

        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=SHEET_NAME).execute()
        values = result.get('values', [])

        return pd.DataFrame(values)

    @staticmethod
    def update_google_sheet(spreadsheet_id,sheet_name,range,dataframe):
        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('config/token.pickle'):
            with open('config/token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'config/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('config/token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        service = build('sheets', 'v4', credentials=creds)
        values = dataframe.values.tolist()
        body = {
            'values':values
        }
        SPREADSHEET_ID=spreadsheet_id
        RANGE_NAME=sheet_name + '!' + range
        # Call the Sheets API
        sheet = service.spreadsheets()
        request = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
                                    range=RANGE_NAME,valueInputOption='USER_ENTERED',body=body)
        response = request.execute()
