from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


class GoogleSheetsAPI(object):

    def __init__(self, spreadsheet_id):
        self.SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
        self.CLIENT_SECRET_FILE = 'client_secret.json'
        self.APPLICATION_NAME = 'Google Sheets API Python Quickstart'
        self.spreadsheet_id = spreadsheet_id
        self.sheet_ids = self.get_sheet_ids()

    # Stock function from Google fetch user credentials, or generate/regenerate fresh credentials if stale
    def get_credentials(self):
        """Gets valid user credentials from storage.
        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.
        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'sheets.googleapis.com-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials


    # Stock function from Google to read values of a declared range from a fixed spreadsheet
    def read_range(self, range_name, dimension="ROWS", render="FORMATTED_VALUE"):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        service = discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)

        spreadsheet_id = self.spreadsheet_id
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=range_name, majorDimension=dimension, valueRenderOption=render).execute()
        values = result.get('values', [])

        if not values:
            return [[0]]
        else:
            return values

    # Stock function from Google to write values into a declared range in a fixed spreadsheet
    def write_range(self, range_name, values, dimension="ROWS", value_input_option="USER_ENTERED"):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        service = discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)

        spreadsheet_id = self.spreadsheet_id 
        body = {"values": values,
                "majorDimension": dimension}
        result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption=value_input_option, body=body).execute()    

    # Produce a dict of all sheet_ids by sheet name
    def get_sheet_ids(self):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        service = discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)

        spreadsheet_id = self.spreadsheet_id
        response = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        sheet_ids = {}
        for sheet in response["sheets"]:
            sheet_ids[sheet["properties"]["title"]] = sheet["properties"]["sheetId"]
        return sheet_ids


    # Insert blank lines into a sheet by sheet_id
    def insert_lines(self, sheetId, line_location, number_of_lines=1, dimension="ROWS"):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        service = discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)

        spreadsheet_id = self.spreadsheet_id
        requests = [{
            "insertDimension": {
                "range": {
                    "sheetId": sheetId,
                    "dimension": dimension,
                    "startIndex": line_location - 1,
                    "endIndex": line_location - 1 + number_of_lines
                    },
                "inheritFromBefore": False
                }
            }]
        body = {"requests": requests}
        response = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id,
                                                      body=body).execute()


     # Make bulk changes by specific request as a list of dicts
    def change_formatting(self, requests):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        service = discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)

        spreadsheet_id = self.spreadsheet_id
        body = {"requests": requests}
        response = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id,
                                                      body=body).execute()


    # Clear all values from an entire sheet by sheetID
    def clear_sheet(self, sheetId):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        service = discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)

        spreadsheet_id = self.spreadsheet_id
        requests = [{
            "updateCells": {
                "range": {
                    "sheetId": sheetId
                    },
                "fields": "userEnteredValue"
                }
            }]
        body = {"requests": requests}
        response = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id,
                                                      body=body).execute()