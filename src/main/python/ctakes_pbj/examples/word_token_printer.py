# Should accept cmd line parameters such as: hostname, port, queue name for recieving cas, and queue name for
# sending cas

# These are the lines that ignore the typesystem errors
import warnings


from ctakes_pbj.pbj_receiver import *
from ctakes_pbj.cas_handlers.cas_sentence_printer import *
from ctakes_pbj.pbj_sender import PBJSender
from ctakes_pbj.cas_handlers.pbj_pipeline import PBJPipeline
from ctakes_pbj import arg_parser
args = arg_parser.get_args()


warnings.filterwarnings("ignore")


def main():

    pipeline = PBJPipeline()
    pipeline.add(CasSentencePrinter())
    pipeline.add(PBJSender(args.send_queue, args.host_name, args.port_name, args.password, args.username))
    start_receiver(pipeline, args.receive_queue, args.host_name, args.port_name)


if __name__ == "__main__":
    main()

