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

    @staticmethod
    @abstractmethod
    def count(nds, data):
        pass

    def get_by_id(self, ex_id):
        pass

    def get_by_date(self, from_time, to_time):
        pass


class Expenses(AbstractExpenses):
    def __init__(self, db_url: str, nds: float):
        self.conn = sqlite3.connect(db_url)
        self.cursor = self.conn.cursor()
        self.nds = nds

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

    @staticmethod
    def count(nds, data):
        ex_type, ex_amount = data
        if ex_type == 'tax':
            summ = 0
            for amount in ex_amount:
                summ += amount
            return {
                "all_amount": summ,
                "taxes": summ,
                "without_taxes": 0
            }
        if ex_type == 'without_tax':
            summ = 0
            for amount in ex_amount:
                summ += amount
            return {
                "all_amount": summ,
                "taxes": 0,
                "without_taxes": summ
            }
        if ex_type == 'with_tax':
            summ = 0
            tax_summ = 0
            for amount in ex_amount:
                tax = amount * nds
                summ += amount - tax
                tax += tax
            return {
                "all_amount": ex_amount,
                "taxes": tax_summ,
                "without_taxes": summ
            }

    def get_by_id(self, ex_id):
        sql = '''SELECT type, amount FROM expense WHERE id=(?)'''
        self.cursor.execute(sql, (ex_id,))
        return Expenses.count(self.nds, self.cursor.fetchall())

    def get_by_date(self, from_time, to_time):
        sql = '''SELECT amount FROM expense WHERE datetime BETWEEN (?) and (?)'''
        val = (from_time, to_time)
        self.cursor.execute(sql, val)
        return Expenses.count(self.nds, self.cursor.fetchall())




if __name__ == '__main__':
    test = Expenses(data.DB_URL)

    test.add_expense('eat', 'with_taxes', 12.45)

    test.close_conn()
