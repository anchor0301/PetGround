import requests
import json
from line_notify import LineNotify
import hide_api
from test_class import marketName
###############################    라인 코드

notify = LineNotify(hide_api.ACCESS_TOKEN)
error_notify = LineNotify(hide_api.ERROR_TOKEN)

market = marketName()

def post_message_exit(dog, start_day):
    json_object = {
        "service": 2210077160,
        "message":
           f"안녕하세요. {market.name}입니다.\n\n"
           "[서비스 내역]\n\n"
           f"■ 애견이름: {dog.dog_name}\n"
           f"■ 이용일자 : {start_day}\n"
           f"■ 서비스 :  {dog.service}\n\n"
           "[참고사항]\n\n"
           "호텔 이용 후 구토, 설사, 기운 없음 등의 증상이 보일 수 있으나 이는 휴식을 하면 점차 회복되므로 집에서 푹 쉴 수 있도록 도와주세요. 이용해주셔서 감사합니다.\n\n"
           "[서비스 설문조사]\n\n"
           "고객님께 더 나은 서비스를 제공하기 위해 설문조사를 진행하고 있습니다. 이번에 경험하신 서비스에 대한 소중한 의견을 남겨주세요.\n\n"
           "※ 매월 1일마다 설문에 참여하신 분께 추첨을 통해 기프티콘을 드립니다. (카카오톡 채널에 공지)\n\n"
           f"- 전화문의 및 상담 : {market.phoneNumber}",
        "mobile": f"{dog.phoneNumber}",  # 전송받는 전화번호
        "title": "퇴실 안내",  # 타이틀
        "template": "10011",  # 템플릿 코드
        "buttons": [
            {"name": "서비스 설문조사 참여", "url": "https://forms.gle/sX4iNu3NaDS4beQR6||https://forms.gle/sX4iNu3NaDS4beQR6"}]
    }
    json_string = json.dumps(json_object)
    resp = requests.post('https://talkapi.lgcns.com/request/kakao.json', headers=hide_api.headers, data=json_string)
    print("카카오톡 응답 코드 : %d" % resp.status_code)
    print("response body: %s" % resp.text)
    print("---------------------------")


def post_message_service(dog):
    api_host = 'https://talkapi.lgcns.com/'
    headers = hide_api.headers
    if "호" in dog.service:
        json_object = {
            "service": 2210077160,
            "message":
                f"{dog.reservationDate()}\n"  # 호텔 예약
                f"이름: {dog.dog_name}\n"
                f"견종 : {dog.breed}\n"
                f"서비스 : {dog.service}\n"
                f"전화번호 뒷자리 : {dog.backPhoneNumber}\n"
                f"\n"
                f"■ 아래 준비물 및 주의사항 꼭 확인 부탁드립니다.\n"
                f"\n"
                f"■  『최종 확인』 버튼을 눌러주세요",
            "mobile": f"{dog.phoneNumber}",  # 전송받는 전화번호
            "title": "최종 확인을 눌러주세요",  # 타이틀
            "template": "10005",  # 템플릿 코드
            "buttons": [
                {"name": "최종 확인", "type": "MD"},
                {"name": "가게 위치 보기",
                 "url": f"{market.map_mobile}||{market.map_web}"},
                {"name": "준비물 및 주의사항", "url": f"{market.notice_url}||{market.notice_url}"}]
        }
        json_string = json.dumps(json_object)

    elif "놀" in dog.service:
        json_object = {
            "service": 2210077160,
            "message":
                f"{dog.overNight()}"  # 놀이방 예약
                f"이름: {dog.dog_name}\n"
                f"견종 : {dog.breed}\n"
                f"서비스 : {dog.service}\n"
                f"전화번호 뒷자리 : {dog.backPhoneNumber}\n"
                f"\n"
                f"■ 아래 준비물 및 주의사항 꼭 확인 부탁드립니다.\n"
                f"\n"
                f"■  『최종 확인』 버튼을 눌러주세요",
            "mobile": f"{dog.phoneNumber}",  # 전송받는 전화번호
            "title": "최종 확인을 눌러주세요",  # 타이틀
            "template": "10007",  # 템플릿 코드
            "buttons": [
                {"name": "최종 확인", "type": "MD"},
                {"name": "가게 위치 보기",
                  "url": f"{market.map_mobile}||{market.map_web}"},
                {"name": "준비물 및 주의사항", "url": f"{market.notice_url}||{market.notice_url}"}]
        }

        json_string = json.dumps(json_object)


    elif "유치원" in dog.service:
        json_object = {
            "service": 2210077160,
            "message":
                f"서비스 횟수 : {dog.useTime} 회\n\n"  # 유치원 예약 
                f"이름: {dog.dog_name}\n"
                f"견종 : {dog.breed}\n"
                f"서비스 : {dog.service}\n"
                f"전화번호 뒷자리 : {dog.backPhoneNumber}\n"
                f"\n"
                f"■ 아래 준비물 및 주의사항 꼭 확인 부탁드립니다.\n"
                f"\n"
                f"■  『최종 확인』 버튼을 눌러주세요",
            "mobile": f"{dog.phoneNumber}",  # 전송받는 전화번호
            "title": "최종 확인을 눌러주세요",  # 타이틀
            "template": "10010",  # 템플릿 코드
            "buttons": [
                {"name": "최종 확인", "type": "MD"},
                {"name": "가게 위치 보기",
                 "url": f"{market.map_mobile}||{market.map_web}"},
                {"name": "준비물 및 주의사항", "url": f"{market.notice_url}||{market.notice_url}"}]
        }
        json_string = json.dumps(json_object)

    def req(path, query, method, data={}):
        url = api_host + path


        if method == 'GET':
            return requests.get(url, headers=headers)
        else:
            return requests.post(url, headers=headers, data=json_string)

    resp = req('/request/kakao.json', '', 'post')

    print("카카오톡 응답 코드 : %d \t" % resp.status_code ,end="" )
    print(resp.text)


def create_contact(registered_state, dog):
    # 등록상태
    # 0 : 아직 미등록
    # 1 : 이미 등록됨
    # 카카오톡 알림톡 api 실행
    post_message_service(dog)

    if registered_state:
        print(f"중복된 연락처가 있습니다.")
        send = f"\n등록된 연락처\n"
    else:
        print(f"새로운 연락처를 추가합니다\n")
        send = f"\n새로운 연락처 \n"
    notify.send(send +
                f"\n{dog.to_string()}\n"
                f"\n이름 : {dog.host_name} "
                f"\n연락처 : {dog.phoneNumber}"
                f"\n시작일 : {str(dog.start_day_time)[5:-3]}"
                f"\n종료일 : {str(dog.end_day_time)[5:-3]}")

