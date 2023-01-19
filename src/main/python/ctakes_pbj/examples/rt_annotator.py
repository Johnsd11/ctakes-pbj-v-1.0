from ctakes_pbj.cas_handlers.cas_annotator import *
from ctakes_pbj.pbj_tools.create_type import *
from ctakes_pbj.pbj_tools.ctakes_types import *
from cnlpt.cnlp_pipeline_utils import (
    model_dicts,
    classify_casoid_annotations,
    casoid_to_label_tuples,
    generate_paragraph_casoids,
)

from cnlpt.CnlpModelForClassification import (
    CnlpModelForClassification,
    CnlpConfig,
)

from transformers import AutoConfig, AutoModel


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


class RTAnnotator(CasAnnotator):
    def initialize(self, cas):
        # Required for loading cnlpt models using Huggingface Transformers
        AutoConfig.register("cnlpt", CnlpConfig)
        AutoModel.register(CnlpConfig, CnlpModelForClassification)
        # To replace with logging
        print("Loading Models")
        taggers_dict, out_model_dict = model_dicts(pipeline_args.models_dir)
        print("Models Loaded")
        self.taggers = taggers_dict
        self.out_models = out_models
        self.anchor_task = "rt_doc"

    def process(self, cas):

        #  While we could use ct.create_type to create and add types,
        # for each type lookup the cas array is searched.
        #  So it is faster to get the types first and then create instances with ct.add_type
        # anatomy_type = cas.typesystem.get_type(AnatomicalSiteMention)
        # symptom_type = cas.typesystem.get_type(SignSymptomMention)
        # procedure_type = cas.typesystem.get_type(ProcedureMention)

        # sites = ['breast']
        # findings = ['hernia', 'pain', 'migraines', 'allergies']
        # procedures = ['thyroidectomy', 'exam']

        raw_sents = sorted(cas.select(Sentence), key=lambda s: s.begin)

        def cas_clean_sent(sentence):
            return ctakes_clean(cas, sentence)

        cleaned_sents, sent_maps = map(list, zip(*map(cas_clean_sent, raw_sents)))

        def classify_casoid(casoid_pair):
            """
            Args:
            casoid_pair: paragraph and its CASoid
            Returns:
            paragraph, CASoid with classified annotation windows
            """
            paragraph, casoid = casoid_pair
            return paragraph, classify_casoid_annotations(casoid, self.out_models)

        def get_casoid_label(casoid_pair):
            """
            Args:
            casoid_pair: paragraph and its CASoid
            Returns:
            List of (first span indices, second span indices, relation classification data dictionary)
            """
            paragraph, casoid = casoid_pair
            return casoid_to_label_tuples(paragraph, casoid)

        paragraphs = cleaned_sents

        paragraphs_2_raw_casoids = generate_paragraph_casoids(
            paragraphs, self.taggers, self.anchor_task
        )

        paragraphs_2_classified_cassoids = [
            *map(classify_casoid, paragraphs_2_raw_casoids)
        ]

        casoid_labels = [*map(get_casoid_label, paragraphs_2_classified_cassoids)]

        casoid_proto_entities = enumerate(
            zip(paragraphs_2_classified_cassoids, casoid_labels)
        )
