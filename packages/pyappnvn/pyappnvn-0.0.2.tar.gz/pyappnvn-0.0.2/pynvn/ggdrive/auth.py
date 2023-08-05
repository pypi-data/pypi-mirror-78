from __future__ import print_function
import httplib2
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from google.auth.transport.requests import Request
import pickle
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


class auth:
    def __init__(self,SCOPES ,
                CLIENT_SECRET_FILE =None ,
                APPLICATION_NAME = None):
        self.SCOPES = SCOPES
        self.CLIENT_SECRET_FILE = CLIENT_SECRET_FILE
        self.APPLICATION_NAME = APPLICATION_NAME
    def getCredentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        cwd_dir = os.getcwd()
        credential_dir = os.path.join(cwd_dir,
                                     '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'google-drive-credentials.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, 
                                                            self.SCOPES)

            flow.user_agent = self.APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, 
                                            store, 
                                            flags)

            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, 
                                        store)
            print('Storing credentials to ' + credential_path)
        return credentials
    def creds(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                        'client_secret.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return creds
    