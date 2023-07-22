
from __future__ import print_function

import re
import gspread
from Add_PhoneNumber import hide_api

from apiclient import discovery
from oauth2client import tools
from oauth2client.service_account import ServiceAccountCredentials

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/people.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/contacts'
CLIENT_SECRET_FILE = 'aaaa.json'
APPLICATION_NAME = 'People API Python Quickstart'


###############################    gpread코드    ##############################################################

scopee = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
]
json_file_name = 'ding.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scopee)
gc = gspread.authorize(credentials)

# 스프레스시트 문서 가져오기
doc = gc.open_by_url(hide_api.ding_spreadsheet_url)
# 시트 선택하기
worksheet = doc.worksheet('시트1')

#리스트 -> 딕셔너리 -> 값
last_n = worksheet.col_values(6)
last_a = len(last_n)

list_of_dicts = worksheet.get_all_records()
data_list = []
i = 4
for dic in list_of_dicts[-5:]:  # 튜플 안의 데이터를 하나씩 조회해서


    data_dic = {  # 딕셔너리 형태로
        # 요소들을 하나씩 넣음

        'cust_number': last_a - i,
        'dog_name': list(dic.values())[8],
        'breed': list(dic.values())[9],
        'PhoneNumber': "0"+str(list(dic.values())[5])
    }
    i = i - 1
    data_list.append(data_dic)  # 완성된 딕셔너리를 list에 넣음
