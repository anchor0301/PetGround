import requests
import json
from line_notify import LineNotify
import hide_api
from puppyInfo import service

import os.path
import requests

API_URI = "https://notify-api.line.me/api/notify"


class LineNotify:
    def __init__(self, access_token, name=None):
        """Example:

            notify = LineNotify(ACCESS_TOKEN)
            notify = LineNotify(ACCESS_TOKEN, name="CLAIR")

        :param access_token:
        :param name: If name is set, send a message with the name; [NAME] blah blah..
        """
        self.name = name
        self.accessToken = access_token

        if access_token:
            self.enable = True
            self.headers = {"Authorization": "Bearer " + access_token}
        else:
            self.enable = False
            self.headers = {}

    def on(self):
        """Enable notify"""
        self.enable = True

    def off(self):
        """Disable notify"""
        self.enable = False

    def format(self, message):
        if self.name:
            message = '[{0}] {1}'.format(self.name, message)

        return message

    def send(self, message, image_path=None, sticker_id=None, package_id=None):
        """Examples:

            notify.send("text test")
            notify.send("image test", image_path='./test.jpg')
            notify.send("sticker test", sticker_id=283, package_id=4)
            notify.send("image & sticker test", image_path='./test.jpg', sticker_id=283, package_id=4)

        :param message: string
        :param image_path: string
        :param sticker_id: integer
        :param package_id: integer
        :return:
        """
        if not self.enable:
            return

        files = {}
        params = {"message": self.format(message)}

        if image_path and os.path.isfile(image_path):
            files = {"imageFile": open(image_path, "rb")}

        if sticker_id and package_id:
            params = {**params, "stickerId": sticker_id, "stickerPackageId": package_id}

        requests.post(API_URI, headers=self.headers, params=params, files=files)


###############################    라인 코드

notify = LineNotify(hide_api.PUPPYHOUSE_ACCESS_TOKEN)
error_notify = LineNotify(hide_api.ERROR_TOKEN)

def post_message_service(dog):
    """
    예약시 보내는 메시지
    """
    api_host = 'https://talkapi.lgcns.com/'
    headers = hide_api.headers
    if "호" in dog.service:
        json_object = {
            "service": 2310085523,
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
            "title": "예약 완료",  # 타이틀
            "template": "10030",  # 템플릿 코드
            "buttons": [
                {"name": "최종 확인", "type": "MD"},
                {"name": "가게 위치 보기",
                 "url": "http://kko.to/e7crZhDAs9||http://kko.to/e7crZhDAs9"},
                {"name": "준비물 및 주의사항", "url": "http://wp2102.synology.me:1004/my_house_puppy/notice||http://wp2102.synology.me:1004/my_house_puppy/notice"}]
        }
        json_string = json.dumps(json_object)

    elif "놀" in dog.service:
        json_object = {
            "service": 2310085523,
            "message":
                f"{dog.overNight()}"  # 놀이방 예약
                f"이름: {dog.dog_name}\n"
                f"견종 : {dog.breed}\n"
                f"서비스 : {dog.service}\n"
                f"전화번호 뒷자리 : {dog.backPhoneNumber}\n"
                f"\n"
                f"■ 아래 준비물 및 주의사항 꼭 확인 부탁드립니다.\n"
                f"\n"
                f"■ 『최종 확인』 버튼을 눌러주세요",
            "mobile": f"{dog.phoneNumber}",  # 전송받는 전화번호
            "title": "최종 확인을 눌러주세요",  # 타이틀
            "template": "10028",  # 템플릿 코드
            "buttons": [
                {"name": "최종 확인", "type": "MD"},
                {"name": "가게 위치 보기",
                 "url": "http://kko.to/e7crZhDAs9||http://kko.to/e7crZhDAs9"},
                {"name": "준비물 및 주의사항", "url": "http://wp2102.synology.me:1004/my_house_puppy/notice||http://wp2102.synology.me:1004/my_house_puppy/notice"}]
        }

        json_string = json.dumps(json_object)


    elif "유치원" in dog.service:
        json_object = {
            "service": 2310085523,
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
            "template": "10029",  # 템플릿 코드
            "buttons": [
                {"name": "최종 확인", "type": "MD"},
                {"name": "가게 위치 보기",
                 "url": "http://kko.to/e7crZhDAs9||http://kko.to/e7crZhDAs9"},
                {"name": "준비물 및 주의사항", "url": "http://wp2102.synology.me:1004/my_house_puppy/notice||http://wp2102.synology.me:1004/my_house_puppy/notice"}]
        }
        json_string = json.dumps(json_object)


    def req(path, method):
        url = api_host + path

        # print('HTTP Method: %s' % method)
        # print('Request URL: %s' % url)
        # print('Headers: %s' % headers)
        # print('QueryString: %s' % query)

        if method == 'GET':
            return requests.get(url, headers=headers)
        else:
            print(json_object)
            return requests.post(url, headers=headers, data=json_string)

    resp = req('/request/kakao.json', '', 'post')

    print("카카오톡 응답 코드 : %d \t" % resp.status_code, end="")
    print(resp.text)
    # print("response headers:\n%s" % resp.headers)


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

# dog = service(84)
# post_message_service(dog)


# post_message_service(dog)