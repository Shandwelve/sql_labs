from abc import ABC
from core import database


class BaseCommand(ABC):

    def __init__(self):
        self.database = database
