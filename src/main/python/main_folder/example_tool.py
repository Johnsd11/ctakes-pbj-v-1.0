# Should accept cmd line parameters such as: hostname, port, queue name for recieving cas, and queue name for
# sending cas

from example_word_finder import *
# These are the lines that ignore the typesystem errors
import warnings
import pbj_util
import pbj_receiver
from pbj_sender import *
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
    sentence_printer = JCasSentencePrinter(type_system=TypeSystem)
    pbj_receiver.start_receiver(queue_receive_cas, sentence_printer, type_system=TypeSystem, pbj_sender=pbj_sender)


main()
