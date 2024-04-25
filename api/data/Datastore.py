from abc import ABC, abstractmethod


class DataStore(ABC):
    def __init__(self) -> None:
        pass

    @property
    @abstractmethod
    def tables(self):
        pass

    @abstractmethod
    def check_table_exists(func):
        """To be used as a decorator on CRUD functions to check if table exists

        Args:
            func (_type_): function to be wrapped
        """
        pass

    @abstractmethod
    def get_data(self, table: str, key: str, value: str) -> str:
        pass

    @abstractmethod
    def set_data(self, table: str, key: str, value: str) -> None:
        pass

    @abstractmethod
    def delete_data(self, table: str, key: str, value: str) -> None:
        pass
