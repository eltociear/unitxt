import copy
from typing import Any, Dict, List

from .dataclass import Dataclass, OptionalField


class ReusableGenerator(Dataclass):
    """
    Represents a generator that can be reused multiple times.

    Attributes:
        generator (callable): The generator function to be activated.
        gen_argv (List[Any], optional): List of positional arguments for the generator. Defaults to an empty list.
        gen_kwargs (Dict[str, Any], optional): Dictionary of keyword arguments for the generator. Defaults to an empty dict.
    """

    generator: callable
    gen_argv: List[Any] = OptionalField(default_factory=list)
    gen_kwargs: Dict[str, Any] = OptionalField(default_factory=dict)

    def activate(self):
        return self.generator(*self.gen_argv, **self.gen_kwargs)

    def __iter__(self):
        yield from self.activate()

    def __call__(self):
        yield from iter(self)


class CopyingReusableGenerator(ReusableGenerator):
    """
    Extends the ReusableGenerator to deep copy each instance yielded by the
    generator.

    This ensures that modifications to the yielded instances do not
    affect the original data.
    """

    def __iter__(self):
        for instance in self.activate():
            yield copy.deepcopy(instance)
