from abc import ABC, abstractmethod


class JCasAnnotator(ABC):

    def initialize(self):
        pass

    @abstractmethod
    def process(self, cas, typesystem):
        pass

    def collection_process_complete(self):
        pass
