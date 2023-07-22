import datetime as datetime
from datetime import datetime
from dateutil.parser import parse
import requests
import json
from hide_api import ding_notion_headers, patch_exit_data
existing_end_column = 1
new_phone_number_length = 1


body_data = {
    "page_size": 15,
    "filter": {
        "and": [
            {
                "property": "입실 여부",
                "select": {
                    "equals": "퇴실"
                }
            },
            {
                "property": "퇴실 메시지 전송",
                "checkbox": {
                    "equals": False
                }
            }
        ]
    },
    "sorts": [
        {
            "timestamp": "last_edited_time",
            "direction": "descending"
        }
    ]
}

def rest_exit_database():
    read_url = "https://api.notion.com/v1/databases/5ae1d1a61f5f4efe9f9557d62b9adf5e/query"

    res = requests.request("POST", read_url, headers=ding_notion_headers, data=json.dumps(body_data))
    data = res.json()

    results = data.get("results")
    # 없으면 아무것도 안함
    if "[]" == str(results):
        return False

    for i, dogProfile in enumerate(results):
        # 애견 이름
        result = data.get("results")[i].get("properties").get("이름").get("title")[0].get("text").get("content")

        # 입실시간
        start_day = data.get("results")[i].get("properties").get("입실시간").get("formula").get("string")

        # 애견 순번
        dog_num = int(data.get("results")[i].get("properties").get("순번").get("number"))

        # 애견 페이지 코드
        page_code = data.get("results")[i].get("id")

        print("애견 이름 :  %s \n애견 페이지 : %s\n애견 순번 : %s" % (result, page_code, dog_num))

rest_exit_database()