from itertools import product
from cassis import *

from cassis.typesystem import TYPE_NAME_FS_ARRAY

import numpy as np
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

import jcas_processor
from ctakes_types import *

def get_args_to_rel_map(cas):
    args_to_rel = {}
    for bin_text_rel in cas.select(BinaryTextRelation):
        # thanks to DeepPheAnaforaXMLReader.java
        # arg 1 is guaranteed to be med
        # arg 2 - " - sig
        med_arg = bin_text_rel.arg1.argument
        sig_arg = bin_text_rel.arg2.argument
        args_to_rel[(med_arg, sig_arg)] = bin_text_rel
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
        sig_mentions = cas.select_covered(EntityMention, sentence)
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

        if med_mentions and sig_mentions:
            for med_sig_pair in product(med_mentions, sig_mentions):
                if med_sig_pair in args_to_rel.keys():
                    med_sig_rel = args_to_rel[med_sig_pair]
                    label = med_sig_rel.category
                    # else:
                    # label = 'None'
                    med_arg, sig_arg = med_sig_pair
                    if med_arg.begin in token_start_position_map and sig_arg.begin in token_start_position_map:
                        med_idx = token_start_position_map[med_arg.begin]
                        sig_idx = token_start_position_map[sig_arg.begin]
                        sent_labels.append((med_idx, sig_idx, label))
        else:
            sent_labels = 'None'
        sent_len = curr_token_idx
        if sent_len > max_sent_len:
            max_sent_len = sent_len
        # print(f"{sent_labels} : {' '.join(base_tokens)}")
        doc_labels.append(sent_labels)
    return doc_labels, max_sent_len


class ExampleCnlptPipeline(jcas_processor.JCasProcessor):

    def __init__(self, type_system):
        AutoConfig.register("cnlpt", CnlpConfig)
        AutoModel.register(CnlpConfig, CnlpModelForClassification)

        self.cases_processed = 0
        self.dev_size = 21
        self.corpus_max_sent_len = 0
        self.total_labels = []
        self.total_preds = []
        # Only need taggers for now
        taggers_dict, out_dict = model_dicts(
            "/home/ch231037/ctakes_pbj_pipeline_dphe_cr/DeepPhe_CR_pipeline_models",
        )
        print("Models loaded")
        self.type_system = type_system
        self.taggers = taggers_dict
        self.out_models = out_dict
        # Hard-coding for now
        self.central_task = "dphe_med"
        self.task_obj_map = {
            'dosage': (MedicationDosageModifier, MedicationDosage),
            'duration': (MedicationDurationModifier, MedicationDuration),
            'form': (MedicationFormModifier, MedicationForm),
            'freq': (MedicationFrequencyModifier, MedicationFrequency),
            'route': (MedicationRouteModifier, MedicationRoute),
            'strength': (MedicationStrengthModifier, MedicationStrength),
        }

    def process_jcas(self, cas):
        raw_sentences = sorted(cas.select(Sentence), key=lambda s: s.begin)
        doc_labels, max_sent_len = get_relex_labels(cas, raw_sentences)
        FSArray = cas.typesystem.get_type(TYPE_NAME_FS_ARRAY)

        if max_sent_len > self.corpus_max_sent_len:
            self.corpus_max_sent_len = max_sent_len

        def get_ctakes_type(ty):
            return cas.typesystem.get_type(ty)

        def get_ctakes_types(type_pair):
            return tuple(map(get_ctakes_type, type_pair))

        ctakes_type_map = {task: get_ctakes_types(type_pair) for task, type_pair in self.task_obj_map.items()}
        modifier_reference_map = {modifier: set() for modifier in list(zip(*ctakes_type_map.values()))[1]}

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

        aligned_sents_and_data = [cleaned_sentences, sentence_maps, axis_idxs_groups, sig_idxs_groups]

        # for task_name, prediction_tuples in predictions_dict.items():
        # for sent, sent_pred_bundle, sent_map, axis_idxs, sig_idxs in zip(*aligned_sents_and_data):
        for task_name, prediction_tuples in predictions_dict.items():
            for sent, sent_map, sent_axis_idxs, sent_sig_idxs in zip(*aligned_sents_and_data):
                # if self.cases_processed < self.dev_size:
                # self.total_preds.extend(prediction_tuples)
                # self.total_labels.extend(doc_labels)
                # self.cases_processed += 1
                print("Sentence:")
                print(sent)
                print(sent_axis_idxs)
                print(sent_sig_idxs)
                tokenized_sent = sent.split()
                med_type = None
                for axis_task, axis_offsets in sent_axis_idxs.items():
                    for axis_offset in axis_offsets:
                        print(f"Axis reached {axis_task} {axis_offset}")
                        axis_begin, axis_end = axis_offset
                        print(f"{axis_task} : {tokenized_sent[axis_begin:axis_end + 1]}")
                        print(f"Local character indices : {sent_map[axis_begin][0], sent_map[axis_end][1]}")

                        medMention = cas.typesystem.get_type(MedicationEventMention)
                        med_type = medMention(
                            begin=sent_map[axis_begin][0],
                            end=sent_map[axis_end][1],
                        )
                        cas.add(med_type)

                for sig_task, sig_offsets in sent_sig_idxs.items():
                    task_label = sig_task.split('_')[-1]
                    attr_mod_type, attr_type = ctakes_type_map(task_label)
                    for sig_offset in sig_offsets:
                        print(f"Sig reached {sig_task} {sig_offset}")
                        sig_begin, sig_end = sig_offset
                        print(f"{sig_task} : {tokenized_sent[sig_begin:sig_end + 1]}")
                        print(f"Local character indices : {sent_map[sig_begin][0], sent_map[sig_end][1]}")

                        attr_mod = attr_mod_type(
                            begin=sent_map[sig_begin][0],
                            end=sent_map[sig_end][1],
                        )

                        attr = attr_type()
                        cas.add(attr_mod)
                        cas.add(attr)
                        modifier_reference_map[attr_mod_type].add(attr_mod_type)
                    attr_mods = FSArray(elements=[list(modifier_reference_map[attr_mod_type])])

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
