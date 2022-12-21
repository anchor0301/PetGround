class Market:

    def __init__(self, name, contacts_auth,spread_sheet_auth,notion_DB,alarm_talk,address,notice):
        self.address = address
        self.name = name
        self.contacts_auth = contacts_auth
        self.spread_sheet_auth = spread_sheet_auth
        self.notion_DB = notion_DB
        self.alarm_talk = alarm_talk
        self.notice = notice




딩굴댕굴_인증키 = "주소를 적고"
딩굴 = Market("딩굴댕굴", "연락처 인증 경로","스프레드 시트 인증 경로","노션 DB주소", "알람톡","집주소","공지사항")


