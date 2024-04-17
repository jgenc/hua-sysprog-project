import json
import pandas as pd


class BettingData:
    def __init__(self, file_path):
        self.file_path = file_path
        self.__load_data()
        self.users, self.events, self.coupons = self.__create_dfs()

    def __load_data(self):
        if "json" in self.file_path:
            js = json.loads(open(self.file_path).read())
            self.data = js
        elif "csv" in self.file_path:
            raise ValueError("File type not currently supported")
        else:
            raise ValueError("File type not supported")

    def __create_dfs(self):
        users = pd.DataFrame(self.data["users"])
        events = pd.DataFrame(self.data["events"])
        coupons = pd.DataFrame(self.data["coupons"])
        return users, events, coupons
