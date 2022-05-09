# 1. Start Receiver,
# 2. Print Sentences from any received cas.


import pbj_receiver
from process_wrapper.jcas_sentence_printer import *
# These are the lines that ignore the typesystem errors
import warnings

warnings.filterwarnings("ignore")
print("receiver running")

sentence_printer = SentencePrinter()

pbj_receiver.start('queue/test', sentence_printer)
