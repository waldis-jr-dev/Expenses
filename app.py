from typing import Generator
from abc import ABC, abstractmethod
import sqlite3
import data


class AbstractExpenses(ABC):

    @classmethod
    @abstractmethod
    def close_conn(cls):
        pass


class Expenses(AbstractExpenses):
    def __init__(self, db_url: str):
        self.conn = sqlite3.connect(db_url)
        self.cursor = self.conn.cursor()

    @classmethod
    def close_conn(cls):
        cls.cursor.close()
        cls.conn.close()


if __name__ == '__main__':
    Expenses(data.DB_URL)
