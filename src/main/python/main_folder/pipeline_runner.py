

class Pipeline:

    def __init__(self):
        self.processors = []

    def add_processor(self, jcas_processor):
        self.processors.append(jcas_processor)

    def run_processors(self, jcas, typesystem):
        for processor in self.processors:
            processor.process_jcas(jcas, typesystem)





