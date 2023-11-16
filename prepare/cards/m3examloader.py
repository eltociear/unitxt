"""M3 Exan quesion answer given background dataset."""


import json
import os

import datasets

_DESCRIPTION = """\
A record here contains background, question, multiple coices for answer, and answer,
9 languages, different files for the different languages
"""

_HOMEPAGE = "https://github.com/DAMO-NLP-SG/M3Exam"

_URL = "/home/dafna/workspaces/downloads/m3_exam/data/text-question/"

_LANGUAGES = ["afrikaans", "chinese", "english", "italian", "javanese", "portuguese", "swahili", "thai", "vietnamese"]


class M3Exam(datasets.GeneratorBasedBuilder):

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(
            name="{}".format(lang),
        )
        for lang in _LANGUAGES
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "question_text": datasets.Value("string"),
                    "background_description": datasets.Value("string"),
                    "answer_text": datasets.Value("string"),
                    "options": [datasets.Value("string")],
                    "language": datasets.Value("string"),
                    "level": datasets.Value("string"),
                    "subject": datasets.Value("string"),
                    "subject_category": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        lang = str(self.config.name)

        data_dir = _URL
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, lang + "-questions-dev.json"),
                    "split": "test",
                },  # this is the smaller file
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(data_dir, lang + "-questions-test.json"),
                    "split": "train",
                },  # this is the bigger one
            ),
            # datasets.SplitGenerator(
            #     name=datasets.Split.VALIDATION,
            #     gen_kwargs={
            #         "filepath": os.path.join(data_dir, lang + "_val.jsonl"),
            #         "split": "validation"
            #     },
            # ),
        ]

    def _generate_examples(self, filepath, split):
        """Yields examples as (key, example) tuples."""

        with open(filepath, encoding="utf-8") as f:
            allrows = json.load(f)
            print(len(allrows))
            for idx_, row in enumerate(allrows, 1):
                # yield idx_, row
                yield idx_, {
                    "question_text": row["question_text"],
                    "background_description": row["background_description"],
                    "answer_text": row["answer_text"],
                    "options": row["options"],
                    "language": row["language"],
                    "level": row["level"],
                    "subject": row["subject"],
                    "subject_category": row["subject_category"],
                }
