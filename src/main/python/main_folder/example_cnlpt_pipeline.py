from itertools import product

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
from create_type import *
from add_modifier import *


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

    def __init__(self):
        AutoConfig.register("cnlpt", CnlpConfig)
        AutoModel.register(CnlpConfig, CnlpModelForClassification)

        self.cases_processed = 0
        self.dev_size = 21
        self.corpus_max_sent_len = 0
        self.total_labels = []
        self.total_preds = []
        # Only need taggers for now
        taggers_dict, out_dict = model_dicts(
            "C:\Patient_private_data\models\cnlpt_models\pipeline_models",
        )
        print("Models loaded")
        self.type_system = None
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

    def process_jcas(self, cas, typesystem):
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

        task_name, prediction_tuples = list(*predictions_dict.items())

        aligned_sents_and_data = [
            cleaned_sentences,
            prediction_tuples,
            sentence_maps,
            axis_idxs_groups,
            sig_idxs_groups,
        ]
        print("sentence loop")
        for sent, sent_rel_tuples, sent_map, sent_axis_idxs, sent_sig_idxs in zip(*aligned_sents_and_data):
            med_type = None

            # relations are of the form (axis_index, sig_index, relation_type)
            # have to be naive and assume no overlapping annotations between
            # types or within types, use these maps to get an IdentifiedAnnotation
            # from a from the beginning index of a _token_ span (not character span)
            axis_idx_mention_map = {}
            sig_idx_mention_map = {}

            # Entities will be in the form
            # {entity_type: [(span1_begin, span1_end),...]
            # i.e. a dictionary where a type is the key and the value
            # is a list of the indices
            print("axis_task")
            for axis_task, axis_offsets in sent_axis_idxs.items():  # Problem Area (Change this to use pbj API)
                for axis_offset in axis_offsets:
                    axis_begin, axis_end = axis_offset

                    # Construct the map of the med event mentions and
                    # add them to the CAS like in the medication strength example

##########################################################################
                    medMentionType = typesystem.get_type(MedicationMention)
                    med_type = add_type(cas, medMentionType, axis_begin, axis_end)
                    axis_idx_mention_map[axis_begin] = med_type

                    # medMention = cas.typesystem.get_type(MedicationEventMention)
                    # med_type = medMention(
                    #     begin=sent_map[axis_begin][0],
                    #     end=sent_map[axis_end][1],
                    # )
                    # axis_idx_mention_map[axis_begin] = med_type
                    # cas.add(med_type)

################################################################################
            print(axis_idx_mention_map)
            print("-------")
            print(sent_sig_idxs.items())
            # Same logic here but for signatures, with a twist for
            # signature type
            for sig_task, sig_offsets in sent_sig_idxs.items():
                print("task_label: ")
                print(sig_task.split('_'))
                task_label = sig_task.split('_')[-1]
                # Use the type map to get Medication____Modifer and Medication____
                # for the appropriate ____ given the task label, e.g.
                # dosage -> MedicationDosageModifer, MedicationDosage etc.
                # this gives a generalized version of the MedicationStrength example
                attr_mod_type, attr_type = ctakes_type_map[task_label]
                modifier_name = "Medication" + task_label[0].upper() + task_label[1:] + "Modifier"
                print("mod name: " + modifier_name)
                medModifierType = typesystem.get_type(modifier_name)

                for sig_offset in sig_offsets:
                    sig_begin, sig_end = sig_offset
                    mod_type = add_modifier(cas, medModifierType, sig_begin, sig_end)
                    sig_idx_mention_map[sig_begin] = mod_type
                    # for attr in attr_type:
                    #     print(attr)
                    #     for mod in attr_mod_type:
                    #         print(mod)
                    #         add_modifier(cas, attr, mod, sig_begin, sig_end)


                    # attr_mod = attr_mod_type(
                    #     begin=sent_map[sig_begin][0],
                    #     end=sent_map[sig_end][1],
                    # )
                    # attr = attr_type()
                    # cas.add(attr_mod)
                    # cas.add(attr)

                    # modifier_reference_map[attr_mod_type].add(attr_mod)
                    # Assume only one mention per mod list.
                    # Couldn't think of a quick and clean way to generalize
                    # this to the assumed aim
                    # attr_mods = FSArray(
                    #     # elements=list(modifier_reference_map[attr_mod_type])
                    #     elements=[attr_mod]
                    # )
                    # attr.mentions = attr_mods
                    # sig_idx_mention_map[sig_begin] = attr_mods

            if not sent_rel_tuples == 'None':
                for axis_idx, sig_idx, rel_label in sent_rel_tuples:
                    # Get the MedicationEventMention
                    # and the Medication____ (with its attached FSArray)
                    # that the relation says it links
                    axis_mention = axis_idx_mention_map[axis_idx]
                    sig_mods = sig_idx_mention_map[sig_idx]
                    # Between problems with maping object attributes
                    # and since we're not in python 3.10 and can't
                    # use Haskell/OCaml/SML style case matching
                    # have to do it this way...
                    sig_label = rel_label.split('_')[-1]
                    if sig_label == "dosage":
                        axis_mention.medicationDosage = sig_mods
                        cas.add(sig_mods)
                    elif sig_label == "duration":
                        axis_mention.medicationDuration = sig_mods
                        cas.add(sig_mods)
                    elif sig_label == "form":
                        axis_mention.medicationForm = sig_mods
                        cas.add(sig_mods)
                    elif sig_label == "frequency":
                        axis_mention.medicationFrequency = sig_mods
                        cas.add(sig_mods)
                    elif sig_label == "route":
                        axis_mention.medicationRoute = sig_mods
                        cas.add(sig_mods)
                    elif sig_label == "strength":
                        axis_mention.medicationStrength = sig_mods
                        cas.add(sig_mods)
        for sent in sorted(cas.select(Sentence), key=lambda s: s.begin):
            medications = sorted(cas.select_covered(MedicationEventMention, sent), key=lambda s: s.begin)
            if medications:
                print(sent.get_covered_text())
                # PROBLEM AREA
                # This is the part that's giving me issues,
                # the hasattr is to prevent errors I got from
                # trying to access the field when it wasn't initialized
                # but the consequence is no attributes are showing up.
                # There are three distinct problems (possibly overlapping but I don't think)
                # in increasing severity:
                # 1. The test notes I picked are just sparse for relations and I'm having a hard time finding stuff
                # 2. The logic in this file for re-inserting the models' discoveries is wrong.
                # 3. I messed up the relation logic in cnlpt when adding logic for returning entities.
                # I think (3) is unlikely since I managed to add the entity logic in a way that didn't modify the
                # relation logic.  And as sparse as they are and as bad as the models are it _does_ find some obvious
                # relations that are good for debugging, so I'm betting on 2
                for i, med in enumerate(medications):
                    print(f"Medication {i}: {med.get_covered_text()}")
                    # These didn't work either
                    # print(med.get_medication_dosage())
                    # print(med.get_medication_duration())
                    # print(med.get_medication_form())
                    # print(med.get_medication_frequency())
                    # print(med.get_medication_route())
                    # print(med.get_medication_strength())
                """
                    if hasattr(med, 'MedicationDosage'):
                        print(f"Dosage {i}: {med.MedicationDosage}")
                    if hasattr(med, 'MedicationDuration'):
                        print(f"Duration {i}: {med.MedicationDuration}")
                    if hasattr(med, 'MedicationForm'):
                        print(f"Form {i}: {med.MedicationForm}")
                    if hasattr(med, 'MedicationFrequency'):
                        print(f"Frequency {i}: {med.MedicationFrequency}")
                    if hasattr(med, 'MedicationRoute'):
                        print(f"Route {i}: {med.MedicationRoute}")
                    if hasattr(med, 'MedicationStrength'):
                        print(f"Strength {i}: {med.MedicationStrength}")
                    """

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
