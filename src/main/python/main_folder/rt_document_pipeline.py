from itertools import product
from functools import reduce

import numpy as np
from cnlpt.CnlpModelForClassification import (
    CnlpModelForClassification,
    CnlpConfig,
)
from cnlpt.cnlp_pipeline_utils import (
    model_dicts,
    get_predictions,
    relex_label_to_matrix,
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
            base_tokens.append("<cr>")
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
                base_tokens.append("<cr>")
            curr_token_idx += 1

        if med_mentions and sig_mentions:
            med_sig_pairs = map(
                lambda s: tuple(sorted(s)), product(med_mentions, sig_mentions)
            )

            for med_sig_pair in med_sig_pairs:
                if med_sig_pair in args_to_rel.keys():
                    med_sig_rel = args_to_rel[med_sig_pair]
                    label = med_sig_rel.category
                    med_arg, sig_arg = med_sig_pair
                    if (
                        med_arg.begin in token_start_position_map
                        and sig_arg.begin in token_start_position_map
                    ):
                        med_idx = token_start_position_map[med_arg.begin]
                        sig_idx = token_start_position_map[sig_arg.begin]
                        first_idx = min(med_idx, sig_idx)
                        second_idx = max(med_idx, sig_idx)
                        sent_labels.append((first_idx, second_idx, label))
        else:
            sent_labels = "None"
        sent_len = curr_token_idx
        if sent_len > max_sent_len:
            max_sent_len = sent_len
        # print(f"{sent_labels} : {' '.join(base_tokens)}")
        doc_labels.append(sent_labels)
    return doc_labels, max_sent_len


# Make sure you use the right dictionaries for the predicted
# so we're not conveniently displaying the predictions
# in terms of the gold entities
def get_text_triples(cas, text_unit, text_unit_labels, axis_offsets, sig_offsets):
    def first_idx_to_full(dict_values):
        return {idx_1: (idx_1, idx_2) for idx_1, idx_2 in dict_values}

    all_offsets_raw = [
        *map(first_idx_to_full, (*axis_offsets.values(), *sig_offsets.values()))
    ]

    def dict_reduce(d1, d2):
        return dict((*d1.items(), *d2.items()))

    all_offsets = reduce(dict_reduce, all_offsets_raw)
    tok_text_unit = ctakes_tokenize(cas, text_unit)

    def idx2span(t):
        idx1, idx2, label = t
        span1 = tok_text_unit[slice(*all_offsets[idx1])]
        span2 = tok_text_unit[slice(*all_offsets[idx2])]
        return span1, span2, label

    return [*map(idx2span, text_unit_labels)]


class RTDocumentPipeline(cas_annotator.CasAnnotator):
    def __init__(self, type_system, eval_set_size=None):
        self.corpus_max_sent_len = -1
        self.total_preds = []
        self.total_labels = []
        self.type_system = type_system
        self.taggers = None
        self.out_models = None
        self.central_task = None
        self.eval_set_size = -1 if eval_set_size is None else eval_set_size
        self.casses_processed = 0
        self.out_tasks = []

    def initialize(self):
        AutoConfig.register("cnlpt", CnlpConfig)
        AutoModel.register(CnlpConfig, CnlpModelForClassification)
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

        cleaned_sentences, sentence_maps = map(
            list, zip(*map(cas_clean_sent, raw_sentences))
        )
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
            mode="eval",
        )

        print("Predictions obtained")

        for task_name, prediction_tuples in predictions_dict.items():
            self.out_tasks.append(task_name)
            if self.casses_processed < self.eval_set_size:
                self.total_preds.extend(prediction_tuples)
                self.total_labels.extend(doc_labels)
                self.casses_processed += 1
            report = cnlp_compute_metrics(
                classifier_to_relex[task_name],
                # Giant relex matrix of the predictions
                np.array(
                    [
                        local_relex(sent_preds, max_sent_len)
                        for sent_preds in prediction_tuples
                    ]
                ),
                # Giant relex matrix of the ground
                # truth labels
                np.array(
                    [
                        local_relex(sent_labels, max_sent_len)
                        for sent_labels in doc_labels
                    ]
                ),
            )

            doc_id = cas.select(DocumentID)[0].documentID
            print(f"scores for note {doc_id}")
            print(cnlp_processors[task_name]().get_labels())
            for score_type, scores in report.items():
                print(f"{score_type} : {scores}")

    def collection_process_complete(self):
        for task_name in self.out_tasks:
            task_processor = cnlp_processors[classifier_to_relex[task_name]]()
            label_list = task_processor.get_labels()
            final_label_map = {label: i for i, label in enumerate(label_list)}

            def final_label_to_relex(label):
                return relex_label_to_matrix(
                    label,
                    final_label_map,
                    self.corpus_max_sent_len,
                )

            report = cnlp_compute_metrics(
                classifier_to_relex[task_name],
                np.array(
                    [
                        *map(
                            final_label_to_relex,
                            self.total_preds,
                        )
                    ]
                ),
                np.array([*map(final_label_to_relex, self.total_labels)]),
            )

            print("Final scores over all notes")
            print(label_list)
            for score_type, scores in report.items():
                print(f"{score_type} : {scores}")
