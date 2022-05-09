import os
import sys

from dataclasses import dataclass, field

from pipelines import ctakes_tok

from pbj_cnlp_utils import (
    model_dicts,
    get_anafora_tags,
    get_sentences_and_labels,
)

from pipelines.CnlpModelForClassification import CnlpModelForClassification, CnlpConfig

from transformers import AutoConfig, AutoModel, HfArgumentParser

SPECIAL_TOKENS = ['<e>', '</e>', '<a1>', '</a1>', '<a2>', '</a2>', '<cr>', '<neg>']

modes = ["inf", "eval"]


@dataclass
class PipelineArguments:
    """
    Arguments pertaining to the models, mode, and data used by the pipeline.
    """
    models_dir: str = field(
        metadata={
            "help": (
                "Path where each entity model is stored "
                "in a folder named after its "
                "corresponding cnlp_processor, "
                "models with a 'tagging' output mode will be run first "
                "followed by models with a 'classification' "
                "ouput mode over the assembled data"
            )
        }
    )
    in_file: str = field(
        metadata={
            "help": (
                "Path to file, with one raw sentence"
                "per line in the case of inference,"
                " and one <label>\t<annotated sentence> "
                "per line in the case of evaluation"
            )
        }
    )
    mode: str = field(
        default="inf",
        metadata={
            "help": (
                "Use mode for full pipeline, "
                "inference, which outputs annotated sentences "
                "and their relation, or eval, "
                "which outputs metrics for a provided set of samples "
                "(requires labels)"
            )
        }
    )
    axis_task: str = field(
        default="dphe_med",
        metadata={
            "help": (
                "key of the task in cnlp_processors "
                "which generates the tag that will map to <a1> <mention> </a1>"
                " in pairwise annotations"
            )
        }
    )

def main():
    parser = HfArgumentParser(PipelineArguments)

    if (
            len(sys.argv) == 2
            and sys.argv[1].endswith(".json")
    ):
        # If we pass only one argument to the script
        # and it's the path to a json file,
        # let's parse it to get our arguments.

        # the ',' is to deal with unary tuple weirdness
        pipeline_args, = parser.parse_json_file(
            json_file=os.path.abspath(sys.argv[1])
        )
    else:
        pipeline_args, = parser.parse_args_into_dataclasses()


    # Required for loading cnlpt models using Huggingface
    AutoConfig.register("cnlpt", CnlpConfig)
    AutoModel.register(CnlpConfig, CnlpModelForClassification)


    taggers_dict, out_model_dict = model_dicts(
        "/home/ch231037/pipeline_models/",
    )

    # Only need raw sentences for inference
    _, _, sentences = get_sentences_and_labels(
        in_file=pipeline_args.in_file,
        mode="inf",
        task_names=out_model_dict.keys(),
    )

    anns = taggers_dict['dphe_med'](
        sentences,
    )

    for ann, sent in zip(anns, sentences):
        _, indices = get_anafora_tags(ann, sent)
        print(sent)
        print(f"indices : {indices}")
        for a,b in indices:
            print(ctakes_tok(sent)[a:b])

if __name__ == "__main__":
    main()