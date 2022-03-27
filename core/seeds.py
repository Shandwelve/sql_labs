from abc import ABC, abstractmethod
from core import database


class BaseSeed(ABC):

    def __init__(self):
        self.database = database

    @abstractmethod
    def run(self):
        pass

