import datetime as datetime
from datetime import datetime

import json
import requests

from def_kakao_post import post_message_exit
from hide_api import notion_headers, patch_data
from puppyInfo import DogInformation

from test_class import marketName


market = marketName()


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


# 데이터베이스 읽기
def read_database(notion_database_id):
    """
    데이터베이스를 읽어서 콘솔에 출력을 한 뒤 현재 폴더 db.json 저장을 합니다.
    """

    read_url = f"https://api.notion.com/v1/databases/{notion_database_id}/query"

    res = requests.request("POST", read_url, headers=notion_headers)
    data = res.json()
    print(res.status_code)
    print(data)
    print(res.text)
    # db.json 생성
    # with open('./db.json', 'w', encoding='utf8') as f:
    #     json.dump(data, f, ensure_ascii=False)


# json 정보를 출력함
def print_item_info(res, dog):
    res = res["properties"]
    print("\n---------------- 응답 결과 ----------------")
    print("타임스탬프\t:  ", datetime.now())
    print("엑셀 행 \t\t:\t" + str(res["순번"]['number']))
    print("전화번호 \t\t: \t" + dog.phoneNumber)
    print("강아지 이름 \t: \t" + res["이름"]["title"][0]['text']['content'])
    print("강아지 정보 \t: \t" + res["성별"]["select"]["name"] + "\t" + res['견종']["select"]["name"], end="\t")
    print(str(res["몸무게"]['number'])+"kg")
    print("서비스 \t\t: \t" + res["서비스"]["select"]['name'])
    print("입실 \t\t: \t" + res['날짜']['date']["start"])
    print("퇴실 \t\t: \t" + res['날짜']['date']["end"])
    print("---------------------------------------\n\n")


# 애견 페이지를 만든다
def create_page(dog):
    create_url = 'https://api.notion.com/v1/pages'
    new_page_data = {
        "parent": {"database_id": f"{market.notion_database_id}"},
        "properties": {
            "이름": {
                "title": [
                    {
                        "text": {
                            "content": f"{dog.dog_name}"
                        }
                    }
                ]
            },
            "서비스": {
                "type": "select",
                "select": {"name": f"{dog.service}"}
            },
            "날짜": {
                "type": "date",
                "date": {"start": f"{dog.start_day_time}+09:00",
                         "end": f"{dog.end_day_time}+09:00"}
            },
            "견종": {
                "type": "select",
                "select": {"name": f"{dog.breed}"}
            },
            "몸무게": {
                "type": "number",
                "number": float(dog.weight)
            },
            "특이사항": {
                "rich_text": [
                    {
                        "text": {
                            "content": f"{dog.Others}"
                        }
                    }
                ]
            },
            "성별": {
                "type": "select",
                "select": {"name": f"{dog.sex}"}
            },
            "입실 여부": {
                "type": "select",
                "select": {"name": "No"}
            }, "순번": {
                "type": "number",
                "number": dog.row_number
            }
        }
    }

    data = json.dumps(new_page_data)

    res = requests.request("POST", create_url, headers=notion_headers, data=data)

    print("노션 응답 코드 :  %s \n" % res.status_code)
    # print(res.json())
    dog.info()


# 오늘 퇴실한 강아지 출력 및
def rest_exit_database():
    read_url = f"https://api.notion.com/v1/databases/{market.notion_database_id}/query"

    res = requests.request("POST", read_url, headers=notion_headers, data=json.dumps(body_data))
    data = res.json()

    results = data.get("results")
    # 없으면 아무것도 안함
    if "[]" == str(results):
        return False

    for i in range(len(results)):
        # 애견 이름
        result = data.get("results")[i].get("properties").get("이름").get("title")[0].get("text").get("content")

        # 입실시간
        start_day = data.get("results")[i].get("properties").get("입실시간").get("formula").get("string")

        # 애견 순번
        dog_num = int(data.get("results")[i].get("properties").get("순번").get("number"))

        # 애견 페이지 코드
        page_code = data.get("results")[i].get("id")

        print("애견 이름 :  %s \n애견 페이지 : %s\n애견 순번 : %s" % (result, page_code, dog_num))

        post_message_exit(DogInformation(dog_num), start_day)
        patch_exit_database(page_code)

    return True


# 노션에 카카오톡 메시지를 체크로 변경함
def patch_exit_database(notion_page_id):
    read_url = f"https://api.notion.com/v1/pages/{notion_page_id}"

    requests.request("PATCH", read_url, headers=notion_headers, data=json.dumps(patch_data))

#dog = DogInformation(17)
#create_page(dog)  # 노션 추가 및 응답 결과 출력
# read_database(notion_databaseId,notion_headers) #테이블 읽기
#rest_exit_database()  # 퇴실한 녀석 찾아 메시지 전송


