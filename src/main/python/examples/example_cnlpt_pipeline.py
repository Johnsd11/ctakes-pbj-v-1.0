import re
import ctakes_const


from process_wrapper import jcas_processor
from ctakes_types import *

from cnlpt.cnlp_pipeline_utils import model_dicts

from cnlpt.CnlpModelForClassification import (
    CnlpModelForClassification,
    CnlpConfig,
)

from transformers import AutoConfig, AutoModel


# Convert from B I O list format
# to 1 2 0 string format for easy splitting
def get_partitions(axis_ann):
    def tag2idx(tag):
        if tag != 'O':
            if tag[0] == 'B':
                return 1
            elif tag[0] == 'I':
                return 2
        # 2 identifies the second
        else:
            return 0
    index_tagged = map(tag2idx, axis_ann)
    return "".join([str(idx) for idx in index_tagged])


def process_ann(annotation):
    span_begin, span_end = 0, 0
    indices = []
    partitions = get_partitions(annotation)
    # Group 1's individually as well as 1's followed by
    # any nummber of 2's, e.g.
    # 00000011111112222121212
    # -> 000000 1 1 1 1 1 1 12222 12 12 12
    for span in filter(None, re.split(r'(12*)', partitions)):
        span_end = len(span) + span_begin
        if span[0] == '1':
            # Get indices in list/string of each span
            # which describes a mention
            indices.append((span_begin, span_end))
        span_begin = span_end
    return indices


def ctakes_tokens(raw_text):
    """
    :param raw_text:
    :return: Text split with _all_ whitespace included
    """
    return re.split(r'(\s+)', raw_text)


def get_map(raw_text):
    """
    :param raw_text (raw string)
    :return: token beginnings in raw string organized by token index
    """
    word_beginnings = []
    begin_idx = 0
    for token in ctakes_tokens(raw_text):
        if not token.isspace():
            word_beginnings.append(begin_idx)
        begin_idx += len(token)
    return word_beginnings


class ExampleCnlptPipeline(jcas_processor.JCasProcessor):

    def __init__(self, type_system):
        AutoConfig.register("cnlpt", CnlpConfig)
        AutoModel.register(CnlpConfig, CnlpModelForClassification)

        # Only need taggers for now
        taggers_dict, _ = model_dicts(
            # Hardcoded for now
            "C:\\Users\\ch229935\\Documents\\pipeline_models\\",
        )
        self.type_system = type_system
        self.taggers = taggers_dict
        # Hard-coding for now
        self.central_task = 'dphe_med'

    def process_jcas(self, cas):
        for sentence in cas.select(Sentence):

            # cache for writing mentions from
            # the same sentence to cas
            text = sentence.get_covered_text()
            sent_begin = sentence.begin
            sent_len = len(text)
            central_tagger = self.taggers[self.central_task]
            central_ann = central_tagger(text)
            word_begins = get_map(text)
            central_indices = process_ann(central_ann)

            # Only run cas editing for central
            # task and tagging/cas editing for
            # other tasks if central task has hits
            if len(central_indices) > 0:
                self.process_portion(
                    cas,
                    self.central_task,
                    central_indices,
                    word_begins,
                    sent_begin,
                    sent_len,
                )
                for task_name, sig_tagger in self.taggers.items():
                    if task_name != self.central_task:

                        sig_ann = sig_tagger(text)
                        sig_indices = process_ann(sig_ann)

                        self.process_portion(
                            cas,
                            task_name,
                            sig_indices,
                            word_begins,
                            sent_begin,
                            sent_len,
                        )

    # portion is cTAKES terminology neural whereas
    # segment and sentence aren't
    def process_portion(
            self,
            cas,
            task_name,
            indices,
            word_begins,
            sent_begin,
            sent_len
    ):

        med_mention = self.type_system.get_type(MedicationMention)
        sig_mention = self.type_system.get_type(EventMention)

        word_begins_end = len(word_begins)
        for a, b in indices:
            start = word_begins[a] + sent_begin
            # word begins handles everything except for final index
            # (due to python slices vs indexing weirdness)
            local_end = word_begins[b] if b < word_begins_end else sent_len
            end = local_end + sent_begin - 1

            # Right now just dealing with medication
            # and signature mentions
            if task_name == self.central_task:
                mention = med_mention(begin=start, end=end)
                mention.typeID = ctakes_const.NE_TYPE_ID_DRUG
            else:
                mention = sig_mention(begin=start, end=end)
            cas.add_annotation(mention)
