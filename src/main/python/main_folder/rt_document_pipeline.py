import operator
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
from collections import defaultdict

import cas_annotator
from ctakes_types import *


def get_args_to_rel_map(cas):
    args_to_rel = {}
    for bin_text_rel in cas.select(BinaryTextRelation):
        # As with the medications
        # arg 1 is guaranteed to be a dose (MedicationMention)
        med_arg = bin_text_rel.arg1.argument
        sig_arg = bin_text_rel.arg2.argument
        args_to_rel[
            tuple(sorted((med_arg, sig_arg), key=lambda s: s.begin))
        ] = bin_text_rel
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
    axis_offset_dicts = []
    sig_offset_dicts = []
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

        axis_offset_dicts.append(
            {
                "dosage": [
                    (
                        token_start_position_map[med_mention.begin],
                        token_start_position_map[med_mention.end],
                    )
                    for med_mention in med_mentions
                ]
            }
        )
        sig_offset_dicts.append(
            {
                "signature": [
                    (
                        token_start_position_map[sig_mention.begin],
                        token_start_position_map[sig_mention.end],
                    )
                    for sig_mention in sig_mentions
                ]
            }
        )

        if not (med_mentions and sig_mentions):
            sent_labels = "None"
        else:
            med_sig_pairs = map(
                lambda p: tuple(sorted(p, key=lambda s: s.begin)),
                product(med_mentions, sig_mentions),
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
        sent_len = curr_token_idx
        if sent_len > max_sent_len:
            max_sent_len = sent_len
        doc_labels.append(sent_labels)
    return doc_labels, axis_offset_dicts, sig_offset_dicts, max_sent_len


# Make sure you use the right dictionaries for the predicted
# so we're not conveniently displaying the predictions
# in terms of the gold entities
def get_text_triples(cas, text_unit, text_unit_labels, axis_offsets, sig_offsets):
    print(text_unit)
    print(text_unit_labels)
    print(axis_offsets)
    print(sig_offsets)
    text_unit_labels = [] if text_unit_labels == "None" else text_unit_labels

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
        print(t)
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
        self.doc_reports = []
        self.gold_cas_triple_sets = defaultdict(set)
        self.pred_cas_triple_sets = defaultdict(set)
        self.total_f1 = []

    def initialize(self):
        AutoConfig.register("cnlpt", CnlpConfig)
        AutoModel.register(CnlpConfig, CnlpModelForClassification)
        taggers_dict, out_dict = model_dicts(
            "/home/ch231037/rt_pipeline_models",
        )
        print("Models loaded")
        self.taggers = taggers_dict
        self.out_models = out_dict
        # Hard-coding for now
        self.central_task = "rt_dose"

    def populate_triples(
        self, cas, cas_labels, axis_offset_dicts, sig_offset_dicts, mode="gold"
    ):
        doc_id = cas.select(DocumentID)[0].documentID
        unit_level_cas_data = [
            sorted(cas.select(Sentence), key=lambda s: s.begin),
            cas_labels,
            axis_offset_dicts,
            sig_offset_dicts,
        ]

        def get_local_triples(text, labels, axis_offsets, sig_offsets):
            return get_text_triples(cas, text, labels, axis_offsets, sig_offsets)

        local_triples = set(
            reduce(
                lambda l1, l2: (*l1, *l2),
                map(lambda u: get_local_triples(*u), zip(*unit_level_cas_data)),
            )
        )
        if mode == "gold":
            self.gold_cas_triple_sets[doc_id] = local_triples
        elif mode == "pred":
            self.pred_cas_triple_sets[doc_id] = local_triples

    def process(self, cas):
        doc_id = cas.select(DocumentID)[0].documentID
        raw_sentences = sorted(cas.select(Sentence), key=lambda s: s.begin)
        (
            doc_labels,
            gold_axis_offset_dicts,
            gold_sig_offset_dicts,
            max_sent_len,
        ) = get_relex_labels(cas, raw_sentences)
        if max_sent_len > self.corpus_max_sent_len:
            self.corpus_max_sent_len = max_sent_len

        self.populate_triples(
            cas, doc_labels, gold_axis_offset_dicts, gold_sig_offset_dicts, mode="gold"
        )

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
            if not isinstance(self.total_f1, list):
                self.total_f1 = [0] * len(cnlp_processors[task_name]().get_labels())
            # Only one out task for now so _currently_ I can
            # afford to be naive
            # (by extensionality this might work as a definition of
            # naivety...)

            self.populate_triples(
                cas, prediction_tuples, axis_idxs_groups, sig_idxs_groups, mode="pred"
            )

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
                        local_relex(sent_preds, max_sent_len, mode="pred")
                        for sent_preds in prediction_tuples
                    ]
                ),
                # Giant relex matrix of the ground
                # truth labels
                np.array(
                    [
                        local_relex(sent_labels, max_sent_len, mode="gold")
                        for sent_labels in doc_labels
                    ]
                ),
            )

            print(f"scores for note {doc_id}")
            print(cnlp_processors[task_name]().get_labels())
            for score_type, scores in report.items():
                if score_type == "f1":
                    temp = [*map(operator.add, zip(self.total_f1, scores))]
                    self.total_f1 = temp
                    print(f"class averaged f1 : {sum(scores) / len(scores)}")
                print(f"{score_type} : {scores}")

    def collection_process_complete(self):
        for task_name in self.out_tasks:
            task_processor = cnlp_processors[classifier_to_relex[task_name]]()
            label_list = task_processor.get_labels()
            final_label_map = {label: i for i, label in enumerate(label_list)}

            def final_label_pred(label):
                return relex_label_to_matrix(
                    label,
                    final_label_map,
                    self.corpus_max_sent_len,
                    mode="pred",
                )

            def final_label_gold(label):
                return relex_label_to_matrix(
                    label,
                    final_label_map,
                    self.corpus_max_sent_len,
                    mode="gold",
                )

            report = cnlp_compute_metrics(
                classifier_to_relex[task_name],
                np.array(
                    [
                        *map(
                            final_label_pred,
                            self.total_preds,
                        )
                    ]
                ),
                np.array([*map(final_label_gold, self.total_labels)]),
            )

            print("Final scores over all notes")
            print(label_list)
            for score_type, scores in report.items():
                if score_type != "f1":
                    print(f"{score_type} : {scores}")
                else:
                    print(
                        f"class averaged corpus level f1 : {sum(scores) / len(scores)}"
                    )
                    print(
                        f"class averaged (over document averaged) f1 : {sum(self.total_f1) / len(self.total_f1)}"
                    )
                    print(f"corpus level f1 by class : {scores}")
                    print(
                        f"document averaged f1 by class {[*map(lambda s: s / self.casses_processed, self.total_f1)]}"
                    )
