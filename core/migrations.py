from abc import ABC, abstractmethod
from core import database


class BaseMigration(ABC):

    def __init__(self):
        self.database = database

    @abstractmethod
    def up(self):
        pass

    @abstractmethod
    def down(self):
        pass
