from abc import abstractmethod
from typing import Dict

from .artifact import Artifact
from .collections import ListCollection


class Instruction(Artifact):
    """
    @TODO: add docs
    """

    @abstractmethod
    def __call__(self) -> str:
        pass


class TextualInstruction(Instruction):
    """
    @TODO: add docs
    """

    text: str

    def __call__(self) -> str:
        return self.text

    def __repr__(self):
        return self.text


class InstructionsList(ListCollection):
    """
    @TODO: add docs
    """

    def verify(self):
        for instruction in self.items:
            assert isinstance(instruction, Instruction)


class InstructionsDict(Dict):
    """
    @TODO: add docs
    """

    def verify(self):
        for key, instruction in self.items():
            assert isinstance(instruction, Instruction)
