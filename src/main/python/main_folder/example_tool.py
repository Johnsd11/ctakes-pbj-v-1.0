# Should accept cmd line parameters such as: hostname, port, queue name for recieving cas, and queue name for
# sending cas

from example_word_finder import *
# These are the lines that ignore the typesystem errors
import warnings
import pbj_util
import pbj_receiver_v2
from pbj_sender_v2 import *
from jcas_sentence_printer import *


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
    pbj_sender = PBJSender(queue_send_cas)
    sentence_printer = JCasSentencePrinter()
    pbj_receiver_v2.start_receiver(sentence_printer, queue_receive_cas)


main()
