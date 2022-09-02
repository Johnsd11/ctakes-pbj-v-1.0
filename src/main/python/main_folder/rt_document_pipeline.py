from itertools import product

import numpy as np
from cassis.typesystem import TYPE_NAME_FS_ARRAY
from cnlpt.CnlpModelForClassification import (
    CnlpModelForClassification,
    CnlpConfig,
)
from cnlpt.cnlp_pipeline_utils import (
    model_dicts,
    get_predictions,
)
from cnlpt.cnlp_processors import (
    cnlp_processors,
    cnlp_compute_metrics,
    classifier_to_relex,
)
from transformers import AutoConfig, AutoModel

import cas_annotator
from ctakes_types import *


def get_args_to_rel_map(cas):
    args_to_rel = {}
    for bin_text_rel in cas.select(BinaryTextRelation):
        # As with the medications
        # arg 1 is guaranteed to be a dose (MedicationMention)
        med_arg = bin_text_rel.arg1.argument
        sig_arg = bin_text_rel.arg2.argument
        args_to_rel[tuple(sorted((med_arg, sig_arg)))] = bin_text_rel
    return args_to_rel


def ctakes_tokenize(cas, sentence):
    return sorted(cas.select_covered(BaseToken, sentence), key=lambda t: t.begin)


def ctakes_clean(cas, sentence):
    base_tokens = []
    token_map = []
    newline_tokens = cas.select_covered(NewlineToken, sentence)
    newline_token_indices = {(item.begin, item.end) for item in newline_tokens}

    for base_token in ctakes_tokenize(cas, sentence):
        if (base_token.begin, base_token.end) not in newline_token_indices:
            base_tokens.append(base_token.get_covered_text())
            token_map.append((base_token.begin, base_token.end))
        else:
            base_tokens.append('<cr>')
    return " ".join(base_tokens), token_map


def get_relex_labels(cas, sentences):
    doc_labels = []
    args_to_rel = get_args_to_rel_map(cas)
    max_sent_len = 0
    for sentence in sentences:
        sent_labels = []
        med_mentions = cas.select_covered(MedicationMention, sentence)
        # Changed from medications
        sig_mentions = cas.select_covered(IdentifiedAnnotation, sentence)
        newline_tokens = cas.select_covered(NewlineToken, sentence)
        newline_token_indices = {(item.begin, item.end) for item in newline_tokens}

        token_start_position_map = {}
        curr_token_idx = 0
        base_tokens = []

        for base_token in ctakes_tokenize(cas, sentence):
            if (base_token.begin, base_token.end) not in newline_token_indices:
                if base_token.begin in token_start_position_map.keys():
                    ValueError("Two tokens start with the same index")
                token_start_position_map[base_token.begin] = curr_token_idx
                base_tokens.append(base_token.get_covered_text())
            else:
                base_tokens.append('<cr>')
            curr_token_idx += 1

        med_sig_pairs = map(lambda s: tuple(sorted(s)), product(med_mentions, sig_mentions))

        if med_mentions and sig_mentions:
            for med_sig_pair in med_sig_pairs:
                if med_sig_pair in args_to_rel.keys():
                    med_sig_rel = args_to_rel[med_sig_pair]
                    label = med_sig_rel.category
                    # else:
                    # label = 'None'
                    med_arg, sig_arg = med_sig_pair
                    if med_arg.begin in token_start_position_map and sig_arg.begin in token_start_position_map:
                        med_idx = token_start_position_map[med_arg.begin]
                        sig_idx = token_start_position_map[sig_arg.begin]
                        first_idx = min(med_idx, sig_idx)
                        second_idx = max(med_idx, sig_idx)
                        sent_labels.append((first_idx, second_idx, label))
        else:
            sent_labels = 'None'
        sent_len = curr_token_idx
        if sent_len > max_sent_len:
            max_sent_len = sent_len
        # print(f"{sent_labels} : {' '.join(base_tokens)}")
        doc_labels.append(sent_labels)
    return doc_labels, max_sent_len


class RTDocumentPipeline(cas_annotator.CasAnnotator):

    def __init__(self, type_system):
        self.corpus_max_sent_len = -1
        self.total_preds = []
        self.total_labels = []
        self.type_system = type_system
        self.taggers = None
        self.out_models = None
        self.central_task = None

    def initialize(self):
        AutoConfig.register("cnlpt", CnlpConfig)
        AutoModel.register(CnlpConfig, CnlpModelForClassification)

        self.total_labels = []
        self.total_preds = []
        # Only need taggers for now
        taggers_dict, out_dict = model_dicts(
            "ENTER NAME HERE",
        )
        print("Models loaded")
        self.taggers = taggers_dict
        self.out_models = out_dict
        # Hard-coding for now
        self.central_task = "rt_dose"

    def process(self, cas):
        raw_sentences = sorted(cas.select(Sentence), key=lambda s: s.begin)
        doc_labels, max_sent_len = get_relex_labels(cas, raw_sentences)
        if max_sent_len > self.corpus_max_sent_len:
            self.corpus_max_sent_len = max_sent_len

        def cas_clean_sent(sent):
            return ctakes_clean(cas, sent)
        cleaned_sentences, sentence_maps = map(list, zip(*map(cas_clean_sent, raw_sentences)))
        (
            predictions_dict,
            local_relex,
            axis_idxs_groups,
            sig_idxs_groups,
        ) = get_predictions(
            cleaned_sentences,
            self.taggers,
            self.out_models,
            self.central_task,
            mode='eval',
        )

        print("Predictions obtained")

        for task_name, prediction_tuples in predictions_dict.items():
            report = cnlp_compute_metrics(
                classifier_to_relex[task_name],
                # Giant relex matrix of the predictions
                np.array(
                    [local_relex(sent_preds, max_sent_len) for
                     sent_preds in prediction_tuples]
                ),
                # Giant relex matrix of the ground
                # truth labels
                np.array(
                    [local_relex(sent_labels, max_sent_len) for
                     sent_labels in doc_labels]
                )
            )

            doc_id = cas.select(DocumentID)[0].documentID
            print(f"scores for note {doc_id}")
            print(cnlp_processors[task_name]().get_labels())
            for score_type, scores in report.items():
                print(f"{score_type} : {scores}")
                