import os


from process_wrapper.pipelines.cnlp_processors import (
    cnlp_processors,
    cnlp_output_modes,
    tagging,
    classification
)

from process_wrapper.pipelines.tagging import TaggingPipeline
from process_wrapper.pipelines.classification import ClassificationPipeline
from process_wrapper.pipelines import ctakes_tok

from process_wrapper.pipelines.CnlpModelForClassification import CnlpModelForClassification


from transformers import AutoConfig, AutoTokenizer

from itertools import chain, groupby


SPECIAL_TOKENS = ['<e>', '</e>', '<a1>', '</a1>', '<a2>', '</a2>', '<cr>', '<neg>']


# Get dictionary of entity tagging models/pipelines
# and relation extraction models/pipelines
# both indexed by task names
def model_dicts(models_dir):
    taggers_dict = {}
    out_model_dict = {}

    # For each folder in the model_dir...
    for file in os.listdir(models_dir):
        model_dir = os.path.join(models_dir, file)
        task_name = str(file)
        if os.path.isdir(model_dir) and task_name in cnlp_processors.keys():

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
            if cnlp_output_modes[task_name] == tagging:
                taggers_dict[task_name] = TaggingPipeline(
                    model=model,
                    tokenizer=tokenizer,
                    task_processor=task_processor
                )
            # Add classification pipelines to the classification dictionary
            elif cnlp_output_modes[task_name] == classification:
                out_model_dict[task_name] = ClassificationPipeline(
                    model=model,
                    tokenizer=tokenizer,
                    task_processor=task_processor
                )
            # Tasks other than tagging and sentence/relation classification
            # not supported for now since I wasn't sure how to fit them in
            else:
                ValueError(
                    (
                        "output mode "
                        f"{cnlp_output_modes[task_name]} "
                        "not currently supported"
                    )
                )
    return taggers_dict, out_model_dict

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


# Given a list of integers over {0,1,2}
# and an unannotated sentence,
# return the sentence with <a1> X </a1>
# where X is the span of the split sentence
# corresponding to the span of 1's in the list of integers
# similarly for 2 and <a2>
def get_anafora_tags(annotation, sentence):
    span_begin = 0
    annotated_list = []
    split_sent = ctakes_tok(sentence)
    sig_seen = False
    indices = []
    for tag_idx, span_iter in groupby(get_partitions(annotation)):
        print(f"IN THE LOOP : {tag_idx}")
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

# Get raw sentences, as well as
# dictionaries of labels indexed by output pipeline
# task names
def get_sentences_and_labels(in_file: str, mode: str, task_names):
    task_processors = [cnlp_processors[task_name]() for task_name
                       in task_names]
    idx_labels_dict, str_labels_dict = {}, {}
    if mode == "inf":
        # 'test' let's us forget labels
        # just use the first task processor since
        # _create_examples and _read_tsv are task/label agnostic
        examples = task_processors[0]._create_examples(
            task_processors[0]._read_tsv(in_file),
            "test"
        )
    elif mode == "eval":
        # 'dev' lets us get labels without running into issues of downsampling
        examples = task_processors[0]._create_examples(
            task_processors[0]._read_tsv(in_file),
            "dev"
        )

        def example2label(example):
            if isinstance(example.label, list):
                return [label_map[label] for label in example.label]
            else:
                return label_map[example.label]

        for task_name, task_processor in zip(task_names, task_processors):
            label_list = task_processor.get_labels()
            label_map = {label: i for i, label in enumerate(label_list)}

            if examples[0].label:
                idx_labels_dict[task_name] = [example2label(ex) for ex in examples]
                str_labels_dict[task_name] = [ex.label for ex in examples]
            else:
                ValueError("labels required for eval mode")
    else:
        ValueError("Mode must be either inference or eval")

    if examples[0].text_b is None:
        sentences = [example.text_a for example in examples]
    else:
        sentences = [(example.text_a, example.text_b) for example in examples]

    return idx_labels_dict, str_labels_dict, sentences
