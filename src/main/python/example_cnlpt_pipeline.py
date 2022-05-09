import os
import re
import sys
import numpy as np

from dataclasses import dataclass, field

from process_wrapper.pipelines import ctakes_tok

from pbj_cnlp_utils import (
    model_dicts,
    get_anafora_tags,
)

from process_wrapper.pipelines.cnlp_processors import cnlp_compute_metrics

from process_wrapper.pipelines.CnlpModelForClassification import CnlpModelForClassification, CnlpConfig

from transformers import AutoConfig, AutoModel

SPECIAL_TOKENS = ['<e>', '</e>', '<a1>', '</a1>', '<a2>', '</a2>', '<cr>', '<neg>']

modes = ["inf", "eval"]

from process_wrapper import jcas_processor
from ctakes_types import *

class ExampleCnlptPipeline(jcas_processor.JCasProcessor):

    def __init__(self, type_system):
        self.type_system = type_system

    def process_jcas(self, cas):

        MedMention = self.type_system.get_type(MedicationMention)

        AutoConfig.register("cnlpt", CnlpConfig)
        AutoModel.register(CnlpConfig, CnlpModelForClassification)

        taggers_dict, out_model_dict = model_dicts(
            "/home/ch231037/pipeline_models/",
        )

        for segment in cas.select(Segment):
            text = segment.get_covered_text()

            # Only need raw sentences for inference


            ann = taggers_dict['dphe_med'](
                text,
            )


            _, indices = get_anafora_tags(ann, text)
            print(text)
            print(f"indices : {indices}")
            for a,b in indices:
                print(ctakes_tok(text)[a:b])
                begin_idx = a
                end_idx = b
                tok_sent = ctakes_tok(text)
                start = len(tok_sent[0:begin_idx])
                end = start + end_idx
                medmention = MedMention(begin=start, end=end)
                cas.add_annotation(medmention)

