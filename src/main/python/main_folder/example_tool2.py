# Should accept cmd line parameters such as: hostname, port, queue name for recieving cas, and queue name for
# sending cas


# These are the lines that ignore the typesystem errors
import warnings

import example_word_finder
import pbj_receiver
import pbj_util
from pbj_sender import *

warnings.filterwarnings("ignore")


def main():
    hostname = pbj_util.DEFAULT_HOST
    port = pbj_util.DEFAULT_PORT
    queue_receive_cas = 'test/JavaToPython'
    queue_send_cas = 'test/PythonToJava'

    print(hostname)
    print(port)
    print(queue_receive_cas)
    print(queue_send_cas)

    pbj_sender = PBJSender(queue_send_cas)

    type_system = pbj_util.TypeSystemAccessor().get_type_system()

    word_finder = example_word_finder.ExampleWordFinder(type_system)

    pbj_receiver.start(queue_name=queue_receive_cas, pbj_user_process=word_finder,
                       type_system=type_system, pbj_sender=pbj_sender)


main()
