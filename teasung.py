
import time
existing_end_column = 67

while True:

    time.sleep(5)  # 3분마다 실행
    print("탐색 탐색")
    # 503 에러 방지
    try:
        new_phone_number_length = 66  # 새로 추가된 전화번호를 newPhoneNumberless 저장  B

    except Exception as e:  # 모든 예외의 에러 메시지를 출력할 때는 Exception을 사용
        print("503 에러발생")
        new_phone_number_length = existing_end_column

    if existing_end_column == new_phone_number_length:  # 이미 추가된 전화번호 A 와 새로 등록된 번호 B가 다르면 주소 추가 실행
        continue

    for add_number in reversed(range(0, new_phone_number_length - existing_end_column)):  # 프로그램 실행중 번호 추가 방지
        print("연락처 등록")
