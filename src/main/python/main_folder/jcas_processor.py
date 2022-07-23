# https://www.godaddy.com/engineering/2018/12/20/python-metaclasses/#:~:text=Unfortunately%2C%20Python%20doesn't%20have,in%20order%20to%20be%20initialized.
from abc import ABC, abstractmethod


class JCasProcessor(ABC):

    @abstractmethod
    def process_jcas(self, cas):
        pass

    @abstractmethod
    def __init__(self, type_system):
        self.typesystem = type_system






