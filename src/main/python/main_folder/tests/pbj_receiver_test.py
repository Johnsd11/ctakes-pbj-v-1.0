# 1. Start Receiver,
# 2. Print Sentences from any received cas.
import warnings

from main_folder.cas_sentence_printer import CasSentencePrinter
from main_folder.pbj_receiver_v2 import PbjReceiver
from main_folder.pipeline import Pipeline

# if __name__ == '__main__':
#     if __package__ is None:
#         import sys
#         from os import path
#         sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
#         from pbj_receiver_v2 import *
#         from pipeline_runner import *
#         from jcas_sentence_printer import *
#
#     else:
#         from ..pbj_receiver_v2 import *
#         from ..pipeline import *
#         from ..jcas_sentence_printer import *

warnings.filterwarnings("ignore")

pipeline = Pipeline()
pipeline.add(CasSentencePrinter())
receiver = PbjReceiver(pipeline, "queue/test")
