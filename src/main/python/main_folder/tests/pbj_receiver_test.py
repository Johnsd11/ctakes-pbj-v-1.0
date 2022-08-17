# 1. Start Receiver,
# 2. Print Sentences from any received cas.
if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
        from pbj_receiver_v2 import *
        from pipeline_runner import *
        from jcas_sentence_printer import *

    else:
        from ..pbj_receiver_v2 import *
        from ..pipeline_runner import *
        from ..jcas_sentence_printer import *

import warnings

warnings.filterwarnings("ignore")

pipeline = Pipeline()
pipeline.add_processor(JCasSentencePrinter())
receiver = PbjReceiver(pipeline, 'queue/test')


