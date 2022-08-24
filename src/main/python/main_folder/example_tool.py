# Should accept cmd line parameters such as: hostname, port, queue name for recieving cas, and queue name for
# sending cas

# These are the lines that ignore the typesystem errors
import warnings

import pbj_receiver_v2
from cas_sentence_printer import *
from main_folder.pipeline import Pipeline
from pbj_sender_v2 import *

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
    pipeline = Pipeline()
    pipeline.add(CasSentencePrinter())
    pipeline.add(PBJSender(queue_send_cas))
    pbj_receiver_v2.start_receiver(pipeline, queue_receive_cas)


main()
