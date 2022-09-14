# Should accept cmd line parameters such as: hostname, port, queue name for recieving cas, and queue name for
# sending cas


# These are the lines that ignore the typesystem errors
import warnings

import pbj_receiver_v2
from example_word_finder import ExampleWordFinder
from pbj_sender_v2 import PBJSender
from pipeline import Pipeline

warnings.filterwarnings("ignore")


def main():
    #  TODO - create an example that accepts command line parameters.
    #   e.g. main(argv) getopt("r:s:",["receive=","send="])
    # hostname = pbj_util.DEFAULT_HOST
    # port = pbj_util.DEFAULT_PORT
    queue_receive_cas = 'test/JavaToPython'
    queue_send_cas = 'test/PythonToJava'

    pipeline = Pipeline()
    pipeline.add(ExampleWordFinder())
    pipeline.add(PBJSender(queue_send_cas))
    pbj_receiver_v2.start_receiver(pipeline, queue_receive_cas)


main()
