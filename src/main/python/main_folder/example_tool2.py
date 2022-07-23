# Should accept cmd line parameters such as: hostname, port, queue name for recieving cas, and queue name for
# sending cas


import example_word_finder
# These are the lines that ignore the typesystem errors
import warnings
import pbj_util
import pbj_receiver
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

    type_system_accessor = pbj_util.TypeSystemAccessor()
    type_system_accessor.load_type_system()
    word_finder = example_word_finder.ExampleWordFinder(type_system_accessor.get_type_system())
    pbj_receiver.start(queue_name=queue_receive_cas, pbj_user_process=word_finder,
                       type_system=type_system_accessor.get_type_system(), pbj_sender=pbj_sender)


main()
