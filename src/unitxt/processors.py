import json
import re

from .operator import BaseFieldOperator


class ToString(BaseFieldOperator):
    """
    @TODO: add docs
    """

    def process(self, instance):
        return str(instance)


class ToStringStripped(BaseFieldOperator):
    """
    @TODO: add docs
    """

    def process(self, instance):
        return str(instance).strip()


class ToListByComma(BaseFieldOperator):
    """
    @TODO: add docs
    """

    def process(self, instance):
        output = [x.strip() for x in instance.split(",")]
        return output


class RegexParser(BaseFieldOperator):
    """A processor that uses regex in order to parse a string."""

    regex: str
    termination_regex: str = None

    def process(self, text):
        if self.termination_regex is not None and re.fullmatch(
            self.termination_regex, text
        ):
            return []
        matches = re.findall(self.regex, text)
        return matches


class LoadJson(BaseFieldOperator):
    """
    @TODO: add docs
    """

    def process(self, text):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return []


class ListToEmptyEntitiesTuples(BaseFieldOperator):
    """
    @TODO: add docs
    """

    def process(self, lst):
        try:
            return [(str(item), "") for item in lst]
        except json.JSONDecodeError:
            return []


class DictOfListsToPairs(BaseFieldOperator):
    """
    @TODO: add docs
    """

    position_key_before_value: bool = True

    def process(self, obj):
        try:
            result = []
            for key, values in obj.items():
                for value in values:
                    assert isinstance(value, str)
                    pair = (
                        (key, value) if self.position_key_before_value else (value, key)
                    )
                    result.append(pair)
            return result
        except Exception:
            return []


class TakeFirstNonEmptyLine(BaseFieldOperator):
    """
    @TODO: add docs
    """

    def process(self, instance):
        splitted = str(instance).strip().split("\n")
        if len(splitted) == 0:
            return ""
        return splitted[0].strip()
