# 1. Start Receiver,
# 2. Print Sentences from any received cas.
if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
        from pbj_receiver import *
        from jcas_sentence_printer import *
        from pbj_util import *
        from pbj_sender import *
    else:
        from ..pbj_receiver import *
        from ..jcas_sentence_printer import *
        from ..pbj_util import *
        from ..pbj_sender import *
# These are the lines that ignore the typesystem errors

import warnings

warnings.filterwarnings("ignore")
print("receiver running")

sentence_printer = JCasSentencePrinter(CTAKES_TYPE_SYSTEM)
print("before sender")
pbj_sender1 = PBJSender('queue/test')
print("after sender")
start_receiver('queue/test', sentence_printer, CTAKES_TYPE_SYSTEM, pbj_sender1)

