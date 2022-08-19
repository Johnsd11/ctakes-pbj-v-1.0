# Should accept cmd line parameters such as: hostname, port, queue name for recieving cas, and queue name for
# sending cas


# These are the lines that ignore the typesystem errors
import warnings

import example_word_finder
import pbj_receiver_v2
import pbj_util

warnings.filterwarnings("ignore")


def main():
    hostname = pbj_util.DEFAULT_HOST
    port = pbj_util.DEFAULT_PORT
    queue_receive_cas = 'test/JavaToPython'
    queue_send_cas = 'test/PythonToJava'

    word_finder = example_word_finder.ExampleWordFinder()

    pbj_receiver_v2.start_receiver(word_finder, queue_receive_cas)


main()
