# Should accept cmd line parameters such as: hostname, port, queue name for recieving cas, and queue name for
# sending cas

# These are the lines that ignore the typesystem errors
import warnings


from ctakes_pbj.pbj_receiver import *
from ctakes_pbj.cas_handlers.cas_sentence_printer import *
from ctakes_pbj.pbj_sender import PBJSender
from ctakes_pbj.pbj_tools.pbj_pipeline import Pipeline

warnings.filterwarnings("ignore")


def main():
    #  TODO - create an example that accepts command line parameters.
    #   e.g. main(argv) getopt("r:s:",["receive=","send="])
    # hostname = pbj_util.DEFAULT_HOST
    # port = pbj_util.DEFAULT_PORT
    queue_receive_cas = 'test/JavaToPython'
    queue_send_cas = 'test/PythonToJava'

    pipeline = Pipeline()
    pipeline.add(CasSentencePrinter())
    pipeline.add(PBJSender(queue_send_cas))
    start_receiver(pipeline, queue_receive_cas)


if __name__ == "__main__":
    main()

