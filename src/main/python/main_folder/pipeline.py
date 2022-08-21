class Pipeline:

    def __init__(self):
        self.annotators = []

    def add(self, jcas_processor):
        self.annotators.append(jcas_processor)

    def initialize(self):
        for processor in self.annotators:
            processor.initialize()

    def process(self, jcas, typesystem):
        for processor in self.annotators:
            processor.process(jcas, typesystem)

    def collection_process_complete(self):
        for processor in self.annotators:
            processor.collectionProcessComplete()
