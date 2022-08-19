# Should accept cmd line parameters such as: hostname, port, queue name for recieving cas, and queue name for
# sending cas

from example_cnlpt_pipeline import *
# These are the lines that ignore the typesystem errors
import warnings
from pipeline_runner import *
import pbj_receiver_v2
import pbj_sender_v2
from example_cnlpt_pipeline import ExampleCnlptPipeline
warnings.filterwarnings("ignore")


def main():
    queue_receive_cas = 'test/JavaToPython'

    print(queue_receive_cas)

    pipeline = Pipeline()
    pipeline.add_processor(ExampleCnlptPipeline())
    # Create a new cas processor to translate Eli's med info to cas types
    sender = pbj_sender_v2.PBJSender("test/PythonToJava")
    # pipeline.add_processor(sender)
    pbj_receiver_v2.start_receiver(pipeline, queue_receive_cas)


main()