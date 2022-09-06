# Should accept cmd line parameters such as: hostname, port, queue name for recieving cas, and queue name for
# sending cas

# These are the lines that ignore the typesystem errors
import warnings
from pbj_util import *

import pbj_receiver_v2
from pbj_sender_v2 import *
from rt_document_pipeline import RTDocumentPipeline

warnings.filterwarnings("ignore")


def main():
    hostname = DEFAULT_HOST
    port = DEFAULT_PORT
    queue_receive_cas = "test/JavaToPython"
    queue_send_cas = "test/PythonToJava"

    print(hostname)
    print(port)
    print(queue_receive_cas)
    print(queue_send_cas)

    pbj_sender = PBJSender(queue_send_cas)
    type_system_accessor = TypeSystemAccessor()
    cnlpt_pipe = RTDocumentPipeline(type_system_accessor.get_type_system())
    pbj_receiver_v2.start(
        queue_receive_cas,
        cnlpt_pipe,
        type_system_accessor.get_type_system(),
        pbj_sender,
    )


main()
