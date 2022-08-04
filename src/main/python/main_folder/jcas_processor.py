# https://www.godaddy.com/engineering/2018/12/20/python-metaclasses/#:~:text=Unfortunately%2C%20Python%20doesn't%20have,in%20order%20to%20be%20initialized.
from abc import ABC, abstractmethod
import pbj_sender_v2
import cassis
import pbj_util

# cas = cassis.load_cas_from_xmi(frame.body, typesystem=self.type_system)
# self.jcas_process.process_jcas(cas)
# self.pbj_sender.send_jcas(cas)


class JCasProcessor(ABC):

    @abstractmethod
    def process_jcas(self, cas):
        pass

    @abstractmethod
    def __init__(self, type_system):
        self.typesystem = type_system






