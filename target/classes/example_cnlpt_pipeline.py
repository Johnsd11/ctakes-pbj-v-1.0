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
            return 1
        # 2 identifies the second
        else:
            return 0
    return map(tag2idx, axis_ann)

def process_ann(annotation, sentence):
    span_begin = 0
    annotated_list = []
    split_sent = ctakes_tok(sentence)
    sig_seen = False
    indices = []
    for tag_idx, span_iter in groupby(get_partitions(annotation)):
        span_end = len(list(span_iter)) + span_begin
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

def ctakes_tokens(seg):
    return re.split(r'(\s+)', seg)

def get_map(seg):
    wordBegins  = []
    b=0
    for t in ctakes_tokens(seg):
        # if ( t != whitespace ) {
        if not t.isspace():
            wordBegins.append( b )
        b += len(t)
    return wordBegins

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

        for sentence in cas.select(Sentence):
            text = sentence.get_covered_text()
            seg_begin = sentence.begin
            # Only need raw sentences for inference

            print(text)
            for task_name, tagger in self.taggers.items():

                ann = tagger(text)

                _, indices = process_ann(ann, text)
                # print(f"indices : {indices}")
                for a,b in indices:
                    print(f"Candidate Tokens {ctakes_tok(text)[a:b]}")

                    word_begins = get_map(cas.document_text)
                    start = word_begins[a]
                    end = word_begins[b] - 1

                    if task_name == 'dphe_med':
                        mention = MedMention(begin=start, end=end)
                    else:
                        mention = SigMention(begin=start, end=end)
                    cas.add_annotation(mention)

