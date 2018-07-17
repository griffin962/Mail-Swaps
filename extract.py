"""
Shows basic usage of the Sheets API. Prints values from a Google Spreadsheet.
"""
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import json

# Setup the Sheets API
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('sheets', 'v4', http=creds.authorize(Http()))

# Call the Sheets API
SPREADSHEET_ID = '1u7AGIV4XxwvcGLjH1D7rhnONl0sUDDxP_-8e0kVBVJ0'
LEFT_RANGE = 'B2:Q9'
RIGHT_RANGE = 'B11:Q18'
left = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                           range=LEFT_RANGE).execute()
right = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                            range=RIGHT_RANGE).execute()
values = []
values.append(left.get('values', []))
values.append(right.get('values', []))
data = {'locks': [], 'mailboxes': []}
if not values[0] or not values[1]:
    print('No data found.')
else:
    for side in values:
        for row in side:
            for cell in row:
                split = cell.split()
                if len(split) > 1:
                    mailbox = split[0]
                    combination = split[1].split('-')
                    data['locks'].append(
                        {
                            'room': mailbox,
                            'lock': combination,
                            'originalLock': combination
                        }
                    )
                    data['mailboxes'].append(
                        {
                            'combination': combination,
                            'mailbox': mailbox,
                            'originalMailbox': mailbox
                        }
                    )
    with open('data.json', 'w') as dataFile:
        json.dump(data, dataFile)
