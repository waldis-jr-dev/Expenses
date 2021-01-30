from typing import Generator
from abc import ABC, abstractmethod
import sqlite3
import data
import time


class AbstractExpenses(ABC):
    @abstractmethod
    def close_conn(self):
        pass

    def add_expense(self, ex_name, ex_type, ex_amount):
        pass

    def delete_expense(self, ex_id):
        pass

    def select_by_id(self, ex_id):
        pass

    def select_by_date(self, from_time, to_time):
        pass


class Expenses(AbstractExpenses):
    def __init__(self, db_url: str):
        self.conn = sqlite3.connect(db_url)
        self.cursor = self.conn.cursor()

    def close_conn(self):
        self.cursor.close()
        self.conn.close()

    def add_expense(self, ex_name, ex_type, ex_amount):
        sql = '''INSERT INTO expense VALUES (?, ?, ?, ?)'''
        val = (ex_name, time.time(), ex_type, ex_amount)
        self.cursor.execute(sql, val)
        self.conn.commit()
        return self.cursor.lastrowid

    def delete_expense(self, ex_id):
        sql = '''DELETE FROM expense WHERE id=(?)'''
        self.cursor.execute(sql, (ex_id,))
        self.conn.commit()
        return self.cursor.lastrowid

    def select_by_id(self, ex_id):
        sql = '''SELECT id, name, datetime, type, amount FROM expense WHERE id=(?)'''
        self.cursor.execute(sql, (ex_id,))
        return self.cursor.fetchall()

    def select_by_date(self, from_time, to_time):
        sql = '''SELECT id, name, datetime, type, amount FROM expense WHERE id BETWEEN (?) and (?)'''
        val = (from_time, to_time)
        self.cursor.execute(sql, val)
        return self.cursor.fetchall()




if __name__ == '__main__':
    test = Expenses(data.DB_URL)

    test.add_expense('eat', 'with_taxes', 12.45)

    test.close_conn
