from abc import ABC
from dataclasses import field
from typing import Any, Dict

from datasets import Features, Sequence, Value

from .operator import StreamInstanceOperator


class Validator(ABC):
    """
    @TODO: add docs
    """


class ValidateSchema(Validator, StreamInstanceOperator):
    """
    @TODO: add docs
    """

    schema: Features = None

    def verify(self):
        assert isinstance(
            self.schema, Features
        ), "Schema must be an instance of Features"
        assert self.schema is not None, "Schema must be specified"

    def verify_first_instance(self, instance):
        for s_field in self.standart_fields:
            assert (
                s_field in instance
            ), f'Field "{s_field}" is missing in the first instance'

    def process(
        self, instance: Dict[str, Any], stream_name: str = None
    ) -> Dict[str, Any]:
        return instance


class StandardSchema(Features):
    """
    @TODO: add docs
    """

    def __init__(self):
        super().__init__(
            {
                "source": Value("string"),
                "target": Value("string"),
                "references": Sequence(Value("string")),
                "metrics": Sequence(Value("string")),
                "parser": Value("string"),
                # 'group': Value('string'),
                # 'guidance': Value('string'),
            }
        )


class ValidateStandartSchema:
    """
    @TODO: add docs
    """

    schema: Features = field(default_factory=StandardSchema)
