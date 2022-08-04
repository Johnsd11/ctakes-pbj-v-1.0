# Should accept cmd line parameters such as: hostname, port, queue name for recieving cas, and queue name for
# sending cas

from example_cnlpt_pipeline import *
# These are the lines that ignore the typesystem errors
import warnings
from pbj_util import *

import pbj_receiver
from pbj_sender import *
from jcas_sentence_printer import *
warnings.filterwarnings("ignore")


def main():
    hostname = DEFAULT_HOST
    port = DEFAULT_PORT
    queue_receive_cas = 'test/JavaToPython'
    queue_send_cas = 'test/PythonToJava'

    print(hostname)
    print(port)
    print(queue_receive_cas)
    print(queue_send_cas)
    # start the receiver
    # receiver(queue_receive_cas)
    # once a cas has been received we should start a sender to send the cas
    # start the sender
    pbj_sender = PBJSender(queue_send_cas)
    # pbj_resender = PbjResender(pbj_sender)
    type_system_accessor = TypeSystemAccessor()
    cnlpt_pipe = JCasSentencePrinter(type_system_accessor.get_type_system())
    pbj_receiver.start_receiver(queue_receive_cas, cnlpt_pipe, type_system_accessor.get_type_system(), pbj_sender)


main()