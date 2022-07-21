# Should accept cmd line parameters such as: hostname, port, queue name for recieving cas, and queue name for
# sending cas


from example_word_finder import *
# These are the lines that ignore the typesystem errors
import warnings
from .. import pbj_util, pbj_receiver
from ..pbj_sender import *

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
    word_finder = ExampleWordFinder(type_system_accessor.get_type_system())
    pbj_receiver.start(queue_receive_cas, word_finder, type_system_accessor.get_type_system(), pbj_sender)


main()
