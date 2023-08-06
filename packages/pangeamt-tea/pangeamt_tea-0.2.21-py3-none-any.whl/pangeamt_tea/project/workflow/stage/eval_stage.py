import os
import click
from pangeamt_tea.project.workflow.stage.base_stage import BaseStage
# from pangeamt_tea.project.workflow.workflow import WorkflowAlreadyExists
from pangeamt_nlp.tokenizer.tokenizer_factory import TokenizerFactory
from pangeamt_nlp.truecaser.truecaser import Truecaser
from pangeamt_nlp.processor.pipeline_decoding import PipelineDecoding
from pangeamt_nlp.bpe.bpe import BPE
from sacrebleu import corpus_bleu
from pangeamt_nlp.translation_model.translation_model_factory import (
    TranslationModelFactory,
)
from pangeamt_nlp.seg import Seg
from nteu_translation_engine.engine import Engine


class EvalStage(BaseStage):
    NAME = "eval"
    DIR = "04_evaluated"

    def __init__(self, workflow):
        super().__init__(workflow, self.NAME)

    async def run(self, gpu: int = None, step: int = None):
        project = self.workflow.project
        project_dir = project.config.project_dir
        config = project.config

        workflow_dir = self.workflow.get_dir(project_dir)
        self.stage_dir = os.path.join(workflow_dir, EvalStage.DIR)

        if not os.path.isdir(self.stage_dir):
            os.mkdir(self.stage_dir)

        name = config.translation_model["name"]
        args = config.translation_model["args_decoding"]
        translation_model = TranslationModelFactory.get_class(name)
        model_dir = os.path.join(workflow_dir, "03_trained")
        model_path = None

        sufix = f"{step}.pt" if step else ".pt"

        for file in os.listdir(model_dir):
            if file.endswith(sufix):
                model_path = os.path.join(model_dir, file)
        if model_path is None:
            raise Exception("No model found.")

        self._prepare_dir = os.path.join(workflow_dir, "02_prepared")
        tokenizer = self._init_tokenizer()
        truecaser = Truecaser()
        pipeline = self._init_pipeline()

        src_path = os.path.join(self._prepare_dir, "04_bpe", "test_src.txt")
        tgt_path = os.path.join(self._prepare_dir, "01_raw", "test_tgt.txt")
        out_path = os.path.join(self.stage_dir, "test_output.txt")

        if gpu is not None and gpu > -1:
            args["gpu"] = gpu

        print("Loading model..")

        decoding_model = translation_model(model_path, **args)

        print("Model loaded")

        with open(src_path, "r") as src_file, open(out_path, "w") as out_file:
            batch = []
            segs = []
            with click.progressbar(
                enumerate(src_file),
                length=2000,
                label="Evaluating: ",
            ) as bar:
                for i, src_line in bar:
                    batch.append(src_line)
                    segs.append(Seg(src_line))
                    if (i + 1) % 20 == 0:
                        for translation, seg in zip(
                            decoding_model.translate(batch), segs
                        ):
                            seg.tgt_raw = translation
                            translation = BPE.undo(translation)
                            translation = tokenizer.detokenize(
                                translation.split(" ")
                            )
                            translation = truecaser.detruecase(translation)
                            seg.tgt = translation
                            pipeline.process_tgt(seg)
                            out_file.write(seg.tgt + "\n")
                        batch = []
                        segs = []

        decoding_model = None

        with open(out_path, "r") as sys_file, open(tgt_path, "r") as ref_file:
            final_score = corpus_bleu(sys_file, [ref_file]).score

        print("Bleu score: ", final_score)

        return {
            "Score": final_score
        }

    def _init_pipeline(self) -> PipelineDecoding:
        project = self.workflow.project
        config = project.config
        src_lang = config.src_lang
        tgt_lang = config.tgt_lang
        processors = config.processors

        return PipelineDecoding.create_from_dict(
            src_lang, tgt_lang, processors
        )

    def _init_tokenizer(self):
        project = self.workflow.project
        tgt_tok_name = project.config.tokenizer["tgt"]

        tgt_tokenizer = TokenizerFactory.new(
            project.config.tgt_lang, tgt_tok_name
        )

        return tgt_tokenizer

    async def eval_files(
        self,
        gpu: int,
        step: int,
        src_path: str,
        ref_path: str,
        out_name: str,
        log_file: str,
        debug: bool
    ):
        print("Loading model")
        config = self.workflow.project.config.config_dict
        project = self.workflow.project
        project_dir = project.config.project_dir

        workflow_dir = self.workflow.get_dir(project_dir)
        self.stage_dir = os.path.join(workflow_dir, EvalStage.DIR)
        self._prepare_dir = os.path.join(workflow_dir, "02_prepared")

        if not os.path.isdir(self.stage_dir):
            os.mkdir(self.stage_dir)

        model_dir = os.path.join(workflow_dir, "03_trained")
        model_path = None

        sufix = f"{step}.pt" if step else ".pt"

        for file in os.listdir(model_dir):
            if file.endswith(sufix):
                model_path = os.path.join(model_dir, file)
        if model_path is None:
            raise Exception("No model found.")

        config["translation_engine_server"] = {
            "model_path": model_path,
            "bpe": os.path.join(self._prepare_dir, "bpe_model"),
            "truecaser": os.path.join(self._prepare_dir, "truecase_model"),
            "gpu": True if gpu is not None else False
        }

        if log_file is not None:
            log_path = os.path.join(self.stage_dir, log_file)
        else:
            log_path = None
        engine = Engine(config, log_path, debug)

        if out_name is not None:
            out_path = os.path.join(self.stage_dir, out_name)
        else:
            out_path = os.path.join(self.stage_dir, "test_output.txt")

        with open(src_path, "r") as src_file, open(out_path, "w") as out_file:
            async def _write_to_file(batch):
                for translation in await engine.process_batch(
                    batch
                ):
                    if not translation.endswith("\n"):
                        translation = translation + "\n"
                    out_file.write(translation)
            with open(ref_path, "r") as ref_file:
                batch = []
                with click.progressbar(
                    enumerate(src_file),
                    label="Evaluating: ",
                ) as bar:
                    for i, src_line in bar:
                        batch.append(src_line)
                        if (i + 1) % 20 == 0:
                            await _write_to_file(batch)
                            batch = []
                    if len(batch) != 0:
                        await _write_to_file(batch)
        engine = None

        with open(out_path, "r") as sys_file, open(ref_path, "r") as ref_file:
            final_score = corpus_bleu(sys_file, [ref_file]).score

        print("Score: ", final_score)
