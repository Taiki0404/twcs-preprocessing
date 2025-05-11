from abc import ABCMeta, abstractmethod

from src.generator.dialog import Dialog


class Rule(metaclass=ABCMeta):
    @abstractmethod
    def apply(self, dialog: Dialog) -> bool:
        pass


class NumAuthorsRule(Rule):
    def __init__(self, num_authors: int):
        self.num_authors = num_authors

    def apply(self, dialog: Dialog) -> bool:
        return len(set(dialog.authors)) == self.num_authors
