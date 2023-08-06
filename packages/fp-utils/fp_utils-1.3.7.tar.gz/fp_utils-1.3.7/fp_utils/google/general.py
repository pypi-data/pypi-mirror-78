#Import packages. 
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os

class Google:
    @staticmethod
    def get_google_service(service, creds_path, token_path):
        #Handle scopes. 
        SCOPES = {
            "sheets" : ['https://www.googleapis.com/auth/spreadsheets'], 
            "slides" : ['https://www.googleapis.com/auth/presentations'],
            "drive" : ["https://www.googleapis.com/auth/drive"],
            "gmail" : ["https://www.googleapis.com/auth/gmail.modify"]
        }
        
        # https://developers.google.com/sheets/api/quickstart/python
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    creds_path, SCOPES[service])
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
        
        # Different for sheets and slides. 
        if service=="sheets":
            service = build('sheets', 'v4', credentials=creds, cache_discovery=False)
        elif service=="slides":
            service = build('slides', 'v1', credentials=creds, cache_discovery=False)
        elif service=="drive":
            service = build('drive', 'v3', credentials=creds, cache_discovery=False)
        elif service == "gmail":
            service = build('gmail', 'v1', credentials=creds, cache_discovery=False)
        
        #Return service. 
        return service
    