from abc import ABCMeta, abstractmethod
from typing import Optional

from ..dialog import Dialog


class Rule(metaclass=ABCMeta):
    @abstractmethod
    def apply(self, dialog: Dialog) -> bool:
        pass


class RuleSet:
    def __init__(self, rules: Optional[list[Rule]] = None):
        if rules is None:
            self.rules = []
        else:
            self.rules = rules

    def apply_all(self, dialog: Dialog) -> bool:
        return all(rule.apply(dialog) for rule in self.rules)

    def add(self, rule: Rule):
        self.rules.append(rule)


class NumAuthorsRule(Rule):
    def __init__(self, num_authors: int):
        self.num_authors = num_authors

    def apply(self, dialog: Dialog) -> bool:
        return len(set(dialog.authors_seq)) == self.num_authors


class SequenceLengthRule(Rule):
    def __init__(self, min_length: int, max_length: int):
        self.min_length = min_length
        self.max_length = max_length

    def apply(self, dialog: Dialog) -> bool:
        joined_texts = dialog.join_continuous_texts_by_same_author()
        return self.min_length <= len(joined_texts) <= self.max_length
