import re
from def_gspread import worksheet
from dateutil.parser import parse
import datetime as dt
import datetime
from datetime import datetime
from datetime import timedelta

from def_gspread import get_item_index

"""
        @dog_row_number 엑셀에서 해당 강아지 행 번호

        해당 행 강아지 정보를 가진 객체
    """


class Hotel:
    def __init__(self, dog_row_number):
        dog_information = worksheet.row_values(dog_row_number)
        self.row_number = int(get_item_index(dog_row_number))  # 몇번쨰 행인가
        self.service = dog_information[3]  # 서비스
        self.host_name = dog_information[4]  # 견주이름
        self.phoneNumber = dog_information[5]  # 전체 전화번호
        self.backPhoneNumber = (dog_information[5])[-4:]  # 전화번호 뒷자리

        if dog_information[6]:
            self.start_day_time = parse(dog_information[6])  # 입실일
            self.end_day_time = parse(dog_information[7])  # 퇴실일
            self.start_day = parse((dog_information[6])[:12])
            self.end_day = parse((dog_information[7])[:12])
            self.useTime = "0"
        else:  # 유치원

            now = datetime.now()
            self.start_day_time = str(now.strftime("%Y-%m-%d %H:%M:%S"))
            self.end_day_time = str((now + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"))
            self.useTime = re.sub(r'[^0-9]', '', dog_information[19])  # 횟수

        self.dog_name = dog_information[8]  # 강아지 이름
        self.sex = dog_information[9]  # 강아지 성별
        self.weight = dog_information[10]  # 강아지 몸무게
        self.breed = re.sub(r'\([^)]*\)', '', dog_information[11])  # 견종
        self.Others = dog_information[15]  # 기타 문의사항

    # 메소드 생성시
    def info(self):
        print("추가된 시간\t:  ", datetime.now())
        print("엑셀 행 \t\t:\t", self.row_number)
        print("연락처 이름 \t: \t" + self.to_string())
        print("전화번호 \t\t: \t" + self.phoneNumber)
        print("강아지 이름 \t: \t" + self.dog_name)
        print("강아지 정보 \t: \t" + self.sex + "\t" + self.breed + "\t" + self.weight + "kg")
        print("서비스 \t\t: \t" + self.service)
        print("입실 \t\t: \t", self.start_day_time)
        print("퇴실 \t\t: \t", self.end_day_time)

    def reservationDate(self):
        start_day = self.start_day
        end_day = self.end_day
        # 박 계산
        night = end_day - start_day

        # 일계산
        day = end_day - (start_day + dt.timedelta(days=-1))

        return f"{start_day.strftime('%m월 %d일')} 부터 총{night.days}박 {day.days}일"

    def to_string(self):
        # 견종 중 괄호안의 글자 삭제
        rm_breed = re.sub(r'\([^)]*\)', '', self.breed)

        # 연락처 이름을 저장한다
        # ex) 뚱/포메/호/1234
        print_last_info = f"{self.dog_name}/{rm_breed.rstrip()}/{self.service[0]}/{self.backPhoneNumber}"

        return print_last_info

    def register_time(self):
        start_day_time = self.start_day_time
        start_day_time = start_day_time.strftime("%H:%M")

        return f"{start_day_time}"


class kindSchool(Hotel):
    def __init__(self, dog_row_number):
        super().__init__(dog_row_number)
        dog_information = worksheet.row_values(dog_row_number)

        now = datetime.now()
        self.start_day_time = str(now.strftime("%Y-%m-%d %H:%M:%S"))
        self.end_day_time = str((now + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"))
        self.useTime = re.sub(r'[^0-9]', '', dog_information[19])  # 횟수

    def info(self):
        super().info()
        print("유치원 횟수 \t: \t", self.useTime)


class playroom(Hotel):
    def __init__(self, dog_row_number):
        super().__init__(dog_row_number)

    def overNight(self):
        start_day_time = self.start_day_time
        end_day_time = self.end_day_time

        # 시간 계산
        use_time = ':'.join(str(end_day_time - start_day_time).split(':')[:2])

        start_day_time = start_day_time.strftime("%m월%d일 %H:%M")

        return f"{start_day_time}부터 {use_time}시간\n\n"


def service(dog_row_number):
    services = {
        "유치원": kindSchool,
        "호텔링": Hotel,
        "놀이방": playroom
    }

    how_to_service = worksheet.row_values(dog_row_number)[3]
    if how_to_service in services:
        return services[how_to_service](dog_row_number)

#
# Hotel
# kindSchool
# playroom
