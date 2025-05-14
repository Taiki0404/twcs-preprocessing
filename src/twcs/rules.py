from abc import ABCMeta, abstractmethod

from ..twcs.dialog import Dialog


class Rule(metaclass=ABCMeta):
    @abstractmethod
    def apply(self, dialog: Dialog) -> bool:
        pass


class RuleSet:
    def __init__(self, rules: list[Rule] = []):
        self.rules = rules

    def apply_all(self, dialog: Dialog) -> bool:
        return all(rule.apply(dialog) for rule in self.rules)

    def add(self, rule: Rule):
        self.rules.append(rule)


class NumAuthorsRule(Rule):
    def __init__(self, num_authors: int):
        self.num_authors = num_authors

    def apply(self, dialog: Dialog) -> bool:
        return len(set(dialog.authors)) == self.num_authors
