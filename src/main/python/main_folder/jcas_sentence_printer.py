
import jcas_processor
from ctakes_types import *


class JCasSentencePrinter(jcas_processor.JCasProcessor):

    def __init__(self, type_system):
        pass

    def process_jcas(self, cas):
        for sentence in cas.select(Sentence):
            print(sentence.get_covered_text())
            for token in cas.select_covered(WordToken, sentence):
                # Annotation values can be accessed as properties
                print('Token: Text={0}, begin={1}, end={2}, pos={3}'.format(token.get_covered_text(),
                                                                            token.begin,
                                                                            token.end,
                                                                            token.partOfSpeech))
