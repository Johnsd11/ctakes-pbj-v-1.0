from abc import ABC, abstractmethod


class CasAnnotator(ABC):

    def initialize(self):
        pass

    @abstractmethod
    def process(self, cas):
        pass

    def collection_process_complete(self):
        pass
