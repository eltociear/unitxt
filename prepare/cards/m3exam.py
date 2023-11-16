import os

from prepare.cards.mmlu import (
    multiple_choice_inputs_outputs,
    multiple_choice_preprocess,
)
from src.unitxt.blocks import (
    AddFields,
    FormTask,
    LoadHF,
    MapInstanceValues,
    RenameFields,
    SplitRandomMix,
    TaskCard,
)
from src.unitxt.catalog import add_to_catalog
from src.unitxt.test_utils.card import test_card

# numbering = tuple(str(x) for x in range(200))
numbering = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

langs = ["afrikaans", "chinese", "english", "italian", "javanese", "portuguese", "swahili", "thai", "vietnamese"]
path_to_loader = os.path.join(os.getcwd(), "m3examloader.py")
for lang in langs:
    card = TaskCard(
        loader=LoadHF(path=path_to_loader, name=lang),
        preprocess_steps=[
            SplitRandomMix({"train": "train[90%]", "validation": "train[10%]", "test": "test"}),
            RenameFields(
                field_to_field={
                    "options": "choices",
                    "question_text": "sentence1",
                    "answer_text": "label",
                    "background_description": "context",
                    "subject": "topic",
                }
            ),
            AddFields({"numbers": numbering}),
        ],
        task=FormTask(
            **multiple_choice_inputs_outputs(context=True),
            metrics=["metrics.accuracy"],
        ),
        templates="templates.qa.multiple_choice.context.all",
    )
    if lang == "english":  # langs[0]:
        test_card(card, demos_taken_from="test", debug=True)
    add_to_catalog(card, f"cards.m3exam.{lang}", overwrite=True)
