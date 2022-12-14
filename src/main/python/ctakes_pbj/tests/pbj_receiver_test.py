# 1. Start Receiver,
# 2. Print Sentences from any received cas.
import warnings

from ctakes_pbj.cas_handlers.cas_sentence_printer import CasSentencePrinter
from ctakes_pbj.pbj_receiver import PbjReceiver
from ctakes_pbj.pbj_tools.pbj_pipeline import Pipeline

warnings.filterwarnings("ignore")


def main():

    pipeline = Pipeline()
    pipeline.add(CasSentencePrinter())
    PbjReceiver(pipeline, 'queue/test')


if __name__ == "__main__":
    main()

