import functools
import json
import pandas as pd

from api.data.Datastore import DataStore


class BettingDataDataframe(DataStore):
    def __init__(self, file_path):
        self.file_path = file_path
        self._tables = ["users", "events", "coupons"]
        self._load_data()
        self._users, self._events, self._coupons = self._create_dfs()

    def tables(self):
        return self._tables

    def check_table_exists(func):
        @functools.wraps(func)
        def wrapper(self, table, key, value):
            if table not in self.tables():
                raise ValueError("Table not found")
            return func(self, table, key, value)

        return wrapper

    @check_table_exists
    def get_data(self, table: str, key: str, value: object) -> str:
        if table == "users":
            return self._users.loc[self._users[key] == value]
        elif table == "events":
            return self._events.loc[self._events[key] == value]
        elif table == "coupons":
            return self._coupons.loc[self._coupons[key] == value]

    @check_table_exists
    def set_data(self, table: str, key: str, value: str) -> None:
        raise NotImplementedError("Set not implemented")

    @check_table_exists
    def delete_data(self, table: str, key: str) -> None:
        raise NotImplementedError("Delete not implemented")

    def _load_data(self):
        if "json" in self.file_path:
            js = json.loads(open(self.file_path).read())
            self.data = js
        elif "csv" in self.file_path:
            raise ValueError("File type not currently supported")
        else:
            raise ValueError("File type not supported")

    def _create_dfs(self):
        users = pd.DataFrame(self.data["users"])
        events = pd.DataFrame(self.data["events"])
        coupons = pd.DataFrame(self.data["coupons"])
        return users, events, coupons
