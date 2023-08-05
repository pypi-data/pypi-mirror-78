import gspread
from oauth2client.service_account import ServiceAccountCredentials
def returnclient(scope =  ["https://spreadsheets.google.com/feeds",
                            'https://www.googleapis.com/auth/spreadsheets',
                            "https://www.googleapis.com/auth/drive.file",
                            "https://www.googleapis.com/auth/drive"],
                pathjson =r"C:\Users\nhuan\Desktop\testcode\credentials.json"):
    """ return clent"""

    creds = ServiceAccountCredentials.from_json_keyfile_name(pathjson, scope)
    client = gspread.authorize(creds)
    return client
