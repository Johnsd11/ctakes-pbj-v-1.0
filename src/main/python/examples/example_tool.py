# Should accept cmd line parameters such as: hostname, port, queue name for recieving cas, and queue name for
# sending cas

from example_word_finder import *
# These are the lines that ignore the typesystem errors
import warnings
from .. import pbj_util, pbj_receiver
from ..pbj_sender import *

warnings.filterwarnings("ignore")


def main():
    hostname = DEFAULT_HOST
    port = DEFAULT_PORT
    queue_receive_cas = 'test/receiveQueue'
    queue_send_cas = 'test/sendQueue'

    print(hostname)
    print(port)
    print(queue_receive_cas)
    print(queue_send_cas)
    sentence_printer = JCasSentencePrinter()
    pbj_receiver.start(queue_receive_cas, sentence_printer)


# class PbjResender(jcas_processor.JCasProcessor):
#
#     def __init__(self, pbj_sender):
#         self.pbj_sender = pbj_sender
#
#     def process_jcas(self, cas):
#         for sentence in cas.select('org.apache.ctakes.typesystem.type.textspan.Sentence'):
#             print(sentence.get_covered_text())
#             for token in cas.select_covered('org.apache.ctakes.typesystem.type.syntax.WordToken', sentence):
#                 # Annotation values can be accessed as properties
#                 print('Token: Text={0}, begin={1}, end={2}, pos={3}'.format(token.get_covered_text(),
#                                                                             token.begin,
#                                                                             token.end,
#                                                                             token.partOfSpeech))
#         self.pbj_sender.sendJCas(cas)





# def sender(queue_name):
#     # loading the TypeSystem for the process specified by the user
#     with open('resources/TypeSystem.xml', 'rb') as f:
#         typesystem = load_typesystem(f)
#
#     # Opening the xmi file provided by user and converting it into a cas for
#     with open('tests/test_files/xmi/Peds_FebrileSez_1.xmi', 'rb') as f:
#         cas = load_cas_from_xmi(f, typesystem=typesystem)
#
#     pbj_sender = PBJSender(queue_name)
#     pbj_sender.send(cas)
#     print("sent")


# def receiver(queue_name):
#     print("receiver running")
#     sentence_printer = SentencePrinter()
#     # use queue_receive_cas for the queue name that the user inputs for receiving a cas
#     start(queue_name, sentence_printer)


main()
