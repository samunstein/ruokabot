from generointi.ruoka import Ruoka
from google.oauth2 import service_account
from googleapiclient.discovery import build
import itertools
from statics import SPREADSHEET_ID, RANGE_NAME


def read():
    scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    credentials = service_account.Credentials.from_service_account_file("credentials.json", scopes=scopes)
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])

    data_rows = list(itertools.takewhile(lambda val: val != [], values))
    food_rows = list(filter(lambda row: row != ['Nimi', 'Tyyppi', 'Proteiini', 'Sesonki', 'Annokset', 'Ainekset'], data_rows))

    ruoat = dict(map(lambda r: (r[0], Ruoka(r)), food_rows))
    return ruoat


if __name__ == '__main__':
    read()
