from abc import ABC
from typing import Generator


class Abstract(ABC):
    pass


class Class(Abstract):
    def __init__(self):
        pass


if __name__ == '__main__':
    Class()
