class Pipeline:
    def __init__(self):
        self.annotators = []

    def add(self, cas_processor):
        self.annotators.append(cas_processor)

    def initialize(self):
        for processor in self.annotators:
            processor.initialize()

    def process(self, cas):
        for processor in self.annotators:
            processor.process(cas)

    def collection_process_complete(self):
        for processor in self.annotators:
            processor.collection_process_complete()
