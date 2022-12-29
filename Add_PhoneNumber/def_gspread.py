from __future__ import print_function

import argparse
import os
import json
import gspread
import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.service_account import ServiceAccountCredentials


from test_class import marketName
import hide_api

#-------------market------------

market = marketName()
try:
    import argparsen

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/people.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/contacts'
CLIENT_SECRET_FILE = ".credentials/aaaa.json"
APPLICATION_NAME = 'People API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('./')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'people.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


credentials = get_credentials()
http = credentials.authorize(httplib2.Http())

###############################    gpread코드    ##############################################################

scopee = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
]

json_file_name = market.spreadsheet_auth_file
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scopee)
gc = gspread.authorize(credentials)

# 스프레스시트 문서 가져오기
doc = gc.open_by_url(market.spreadsheet_url)
# 시트 선택하기


worksheet = doc.worksheet('시트1')


def get_item_index(add_number_row):
    return len(worksheet.get("i1:i" + str(add_number_row)))


def create_google_contact(dog):
    """
    구글 주소록에 연락처를 추가하는 api
    :param dog: 스프레드 시트의 강아지 데이터
    :return:
    """

    print(dog.phoneNumber, "번 행의 연락처를 등록합니다.")

    service = discovery.build('people', 'v1', http=http,
                              discoveryServiceUrl='https://people.googleapis.com/$discovery/rest')
    service.people().createContact(body={
        "names": [
            {
                'givenName': f"{dog.to_string()}"
            }
        ],
        "phoneNumbers": [
            {
                'value': f"{dog.phoneNumber}"
            }
        ]
    }).execute()

    print("전화 번호 등록 완료")


#print(worksheet.row_values(2))
