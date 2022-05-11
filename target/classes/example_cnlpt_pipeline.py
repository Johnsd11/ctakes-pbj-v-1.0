import os
import re
import string

from cnlpt.cnlp_processors import (
    cnlp_processors,
    cnlp_output_modes,
    tagging,
)

from cnlpt.pipelines import ctakes_tok
from cnlpt.pipelines.tagging import TaggingPipeline

from cnlpt.cnlp_pipeline_utils import model_dicts

from cnlpt.CnlpModelForClassification import (
    CnlpModelForClassification,
    CnlpConfig,
)

from transformers import AutoConfig, AutoModel, AutoTokenizer

from itertools import groupby

SPECIAL_TOKENS = ['<e>', '</e>', '<a1>', '</a1>', '<a2>', '</a2>', '<cr>', '<neg>']

modes = ["inf", "eval"]

from process_wrapper import jcas_processor
from ctakes_types import *

def get_model(models_dir, target_task_name):
    for file in os.listdir(models_dir):
        model_dir = os.path.join(models_dir, file)
        task_name = str(file)
        if os.path.isdir(model_dir) and task_name in cnlp_processors.keys():
            if task_name == target_task_name:
                # Load the model, model config, and model tokenizer
                # from the model foldner
                config = AutoConfig.from_pretrained(
                    model_dir,
                )

                model = CnlpModelForClassification.from_pretrained(
                    model_dir,
                    config=config,
                )

                # Right now assume roberta thus
                # add_prefix_space = True
                # but want to generalize eventually to
                # other model tokenizers, in particular
                # Flair models for RadOnc
                tokenizer = AutoTokenizer.from_pretrained(
                    model_dir,
                    add_prefix_space=True,
                    additional_special_tokens=SPECIAL_TOKENS,
                )

                task_processor = cnlp_processors[task_name]()

                # Add tagging pipelines to the tagging dictionary

                return TaggingPipeline(
                    model=model,
                    tokenizer=tokenizer,
                    task_processor=task_processor
                )


# Turn two annotations into a list of integers,
# used for fast grouping of indices
# in get_anafora_tags
def get_partitions(axis_ann):
    def tag2idx(tag):
        if tag != 'O':
            if tag.startswith('B'):
                return 1
            elif tag.startswith('I'):
                return 2
        # 2 identifies the second
        else:
            return 0
    index_tagged = map(tag2idx, axis_ann)
    return "".join([str(idx) for idx in index_tagged])

'''
def process_ann_old(annotation, sentence):
    span_begin = 0
    annotated_list = []
    split_sent = ctakes_tok(sentence)
    sig_seen = False
    indices = []
    curr_span_begin = 0
    curr_span_end = 0
    for tag_idx, span_iter in groupby(get_partitions(annotation)):
        span_end = len(list(span_iter)) + span_begin
        if span_end > 0:
            span_end = span_end - 1
        # Get the span of the split sentence
        # which is aligned with the current
        # span of the same integer
        # span = split_sent[span_begin:span_end]
        # ann_span = span
        # Tags are done by type, not order of appearence
        if tag_idx == 1:
            # ann_span = ['<a1>'] + span + ['</a1>']
            indices.append((span_begin, span_end))
        # annotated_list.extend(ann_span)
        span_begin = span_end
    return sentence, indices
'''

def process_ann(annotation):
    span_begin, span_end = 0, 0
    indices = []
    for span in re.split(r'(1{1}2+)|(1{1})', get_partitions(annotation)):
        if span is not None:
        # for span in spans:
            span_end = len(span) + span_begin
            if span.startswith('1'):
                indices.append((span_begin, span_end))
            span_begin = span_end
    return indices


def ctakes_tokens(seg):
    return re.split(r'(\s+)', seg)


def get_map(seg):
    word_begins = []
    b = 0
    for t in ctakes_tokens(seg):
        if not t.isspace():
            word_begins.append(b)
        b += len(t)
    return word_begins


class ExampleCnlptPipeline(jcas_processor.JCasProcessor):

    def __init__(self, type_system):
        AutoConfig.register("cnlpt", CnlpConfig)
        AutoModel.register(CnlpConfig, CnlpModelForClassification)

        taggers_dict, out_model_dict = model_dicts(
            "/home/ch231037/pipeline_models/",
        )
        self.type_system = type_system
        self.taggers = taggers_dict
        self.out_pipes = out_model_dict

    def process_jcas(self, cas):

        MedMention = self.type_system.get_type(MedicationMention)
        SigMention = self.type_system.get_type(EventMention)

        # sentences = [sentence for sentence in cas.select(Sentence)]
        # sentences_text = [sentence.get_covered_text() for sentence in sentences]
        # idx_ann_dict = {}
        central_task = 'dphe_med'
        for sentence in cas.select(Sentence):
            text = sentence.get_covered_text()
            sent_begin = sentence.begin
            central_tagger = self.taggers[central_task]
            central_ann = central_tagger(text)
            central_indices = process_ann(central_ann)
            if len(central_indices) > 0:
                for a, b in central_indices:
                    print(f"Candidate Tokens {ctakes_tok(text)[a:b]}")

                    word_begins = get_map(text)
                    print(
                        (
                            f"word begins  : {word_begins} \n"
                            f"token indices : {a,b} \n"
                        )
                    )
                    if a > len(word_begins) - 1:
                        ValueError(f"Frog pls {a} {word_begins}")
                    start = word_begins[a] + sent_begin
                    if b > len(word_begins) - 1:
                        # just get the last element...
                        end = len(text) + sent_begin - 1
                    else:
                        end = word_begins[b] + sent_begin - 1

                    print(f"document indices {start, end}")
                    # know a priori this is a medication mention
                    mention = MedMention(begin=start, end=end)
                    cas.add_annotation(mention)
                for task_name, sig_tagger in self.taggers.items():
                    if task_name != central_task:
                        sig_ann = sig_tagger(text)
                        sig_indices = process_ann(sig_ann)
                        for a, b in sig_indices:
                            print(f"Candidate Tokens {ctakes_tok(text)[a:b]}")

                            word_begins = get_map(text)
                            print(
                                (
                                    f"word begins  : {word_begins} \n"
                                    f"token indices : {a,b} \n"
                                )
                            )
                            if a > len(word_begins) - 1:
                                ValueError(f"Frog pls {a} {word_begins}")
                            start = word_begins[a] + sent_begin
                            if b > len(word_begins) - 1:
                                # just get the last element...
                                end = len(text) + sent_begin - 1
                            else:
                                end = word_begins[b] + sent_begin - 1

                            print(f"document indices {start, end}")
                            # know a priori this is a sig mention
                            mention = SigMention(begin=start, end=end)
                            cas.add_annotation(mention)


