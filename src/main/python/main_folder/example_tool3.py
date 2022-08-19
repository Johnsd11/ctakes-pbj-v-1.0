# Should accept cmd line parameters such as: hostname, port, queue name for recieving cas, and queue name for
# sending cas

from example_cnlpt_pipeline import *
# These are the lines that ignore the typesystem errors
import warnings
from pbj_util import *

import pbj_receiver_v2
from pbj_sender_v2 import *
from jcas_sentence_printer import *
warnings.filterwarnings("ignore")


def main():
    hostname = DEFAULT_HOST
    port = DEFAULT_PORT
    queue_receive_cas = 'test/JavaToPython'
    queue_send_cas = 'test/PythonToJava'

    print(hostname)

    cnlpt_pipe = JCasSentencePrinter()
    pbj_receiver_v2.start_receiver(cnlpt_pipe, queue_receive_cas)


main()