import datetime as datetime
from datetime import datetime, timedelta

from dateutil.parser import parse
import json
import requests

from hide_api import ding_notion_headers, patch_exit_data, patch_register_check_data, puppyhouse_notion_headers
from puppyInfo import service

# 0 = ding , 1 = mhp
database_id = ["5ae1d1a61f5f4efe9f9557d62b9adf5e", "0cd1f5a289b84f16a0513691d372b4b8"]
db_id = database_id[1]

book_body_data = {
    "page_size": 10,
    "filter": {
        "or": [{
            "property": "서비스",
            "select": {
                "equals": "호텔"
            }
        }, {
            "property": "서비스",
            "select": {
                "equals": "놀이방"
            }
        }],
        "and": [
            {
                "property": "입실 여부",
                "select": {
                    "equals": "No"
                }
            }
        ]
    },
    "sorts": [
        {
            "property": "날짜",
            "direction": "ascending"
        }
    ]
}

# 퇴실한 사람에게 메시지 전송
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

    res = requests.request("POST", read_url, headers=puppyhouse_notion_headers)
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
    print("엑셀 행 \t:\t" + str(res["순번"]['number']))
    print("전화번호 \t: \t" + dog.phoneNumber)
    print("강아지 이름 \t: \t" + res["이름"]["title"][0]['text']['content'])
    print("강아지 정보 \t: \t" + res["성별"]["select"]["name"] + "\t" + res['견종']["select"]["name"], end="\t")
    print(str(res["몸무게"]['number']) + "kg")
    print("서비스 \t\t: \t" + res["서비스"]["select"]['name'])
    print("입실 \t\t: \t" + res['날짜']['date']["start"])
    print("퇴실 \t\t: \t" + res['날짜']['date']["end"])
    print("---------------------------------------\n\n")


# 애견 페이지를 만든다
def create_page(dog):
    create_url = 'https://api.notion.com/v1/pages'
    new_page_data = {
        "parent": {"database_id": f"{db_id}"},
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
                "date": {"start": f"{parse(str(dog.start_day_time)).isoformat()}",
                         "end": f"{parse(str(dog.end_day_time)).isoformat()}"}
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

    res = requests.request("POST", create_url, headers=puppyhouse_notion_headers, data=data)

    print("노션 응답 코드 :  %s \n" % res.status_code)
    print(res.json())
    dog.info()

# dog = service(17)
# book_check_database()ƒ
# create_page(dog)  # 노션 추가 및 응답 결과 출력
# read_database(db_id) #테이블 읽기
# rest_exit_database()  # 퇴실한 녀석 찾아 메시지 전송
# listBookings()
