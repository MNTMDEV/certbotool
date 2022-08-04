
from abc import abstractmethod


class Executable:
    @abstractmethod
    def parse(self):
        pass

    @abstractmethod
    def execute(self):
        pass

    def __init__(self, argv):
        self._argv = argv
        self.parse()
        self.execute()
