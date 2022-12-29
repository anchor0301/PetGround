import json


class Market:

    def __init__(self, json_file_name):
        with open(f'MarketInfoToJson/{json_file_name}.json', encoding="UTF8") as f:
            self.market = json.load(f)
        self.name = self.market["name"]
        self.phoneNumber = self.market["phone_number"]

        self.spreadsheet_url = self.market["spreadsheet_url"]
        self.spreadsheet_auth_file = self.market["auth"][1]["url"]

        self.map_mobile = self.market["alarm_talk"]["buttons"][0]["urls"][0]["url"]
        self.map_web = self.market["alarm_talk"]["buttons"][0]["urls"][1]["url"]

        self.notion_token = self.market["auth"][0]["token"]
        self.notion_headers = self.market["notion"]["headers"]
        self.notice_url = self.market["alarm_talk"]["buttons"][1]["url"]
        self.notion_database_id = self.market["notion"]["id"]


def marketName():
    return Market("my_house_puppy")
    # return Market("Rolling_in_the_dog")
