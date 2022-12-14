# Should accept cmd line parameters such as: hostname, port, queue name for recieving cas, and queue name for
# sending cas


# These are the lines that ignore the typesystem errors
import sys
import warnings

from pbj_receiver import start_receiver
from example_word_finder import ExampleWordFinder
from pbj_sender import PBJSender
from pbj_tools.pbj_pipeline import Pipeline

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
    pipeline.initialize()
    start_receiver(pipeline, queue_receive_cas)


main()

