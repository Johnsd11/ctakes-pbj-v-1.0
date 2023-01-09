# Should accept cmd line parameters such as: hostname, port, queue name for recieving cas, and queue name for
# sending cas


# These are the lines that ignore the typesystem errors
import sys
import warnings

from pbj_receiver import start_receiver
from example_word_finder import ExampleWordFinder
from pbj_sender import PBJSender
from pbj_tools.pbj_pipeline import Pipeline
from ctakes_pbj import arg_parser
args = arg_parser.get_args()

warnings.filterwarnings("ignore")


def main():

    pipeline = Pipeline()
    pipeline.add(ExampleWordFinder())
    pipeline.add(PBJSender(args.send_queue, args.host_name, args.port_name, args.password, args.username))
    pipeline.initialize()
    start_receiver(pipeline, args.receive_queue, args.host_name, args.port_name)


main()

