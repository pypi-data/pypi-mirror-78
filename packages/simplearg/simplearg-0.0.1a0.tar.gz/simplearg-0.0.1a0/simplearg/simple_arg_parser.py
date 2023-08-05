from typing import Dict

from argparse import (
    ArgumentParser,
    Namespace,
    ArgumentDefaultsHelpFormatter,
    _ArgumentGroup,
)
from abc import ABC, abstractproperty, abstractmethod


class SimpleSubCmdIf(ABC):
    @abstractproperty
    def name(self):
        raise NotImplemented()

    @property
    def help(self):
        return ""

    @abstractmethod
    def args(self, parser: ArgumentParser):
        raise NotImplemented()

    @abstractmethod
    def act(self, args: Namespace):
        raise NotImplemented()


class SimpleArgParser:
    def __init__(self, parser: ArgumentParser = None):
        self.parser: ArgumentParser = None
        self.__subparsers: _ArgumentGroup = None
        self.args: Namespace = None
        self.subparsers: Dict[str, "SimpleArgParser"] = {}
        self.parser = parser
        if not parser:
            self.parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)

    @property
    def formatter(self):
        return self.parser.formatter_class

    @formatter.setter
    def formatter(self, value):
        self.parser.formatter_class = value
        for p in self.subparsers.values():
            p.formatter = value

    def add_sub_cmd(self, sub_cmd: SimpleSubCmdIf) -> "SimpleArgParser":
        if not self.__subparsers:
            self.__subparsers = self.parser.add_subparsers(title="commands =>")
            self.__subparsers.required = True
            self.__subparsers.dest = "sub-command"
        sub_parser = self.__subparsers.add_parser(sub_cmd.name, help=sub_cmd.help)
        sub_parser.formatter_class = self.parser.formatter_class
        sub_parser.set_defaults(sub_action=sub_cmd.act)
        sub_cmd.args(sub_parser)
        simple_parser = SimpleArgParser(sub_parser)
        self.subparsers[sub_cmd.name] = simple_parser
        return simple_parser

    def parse(self, args=None, namespace=None) -> Namespace:
        self.args = self.parser.parse_args(args, namespace)
        return self.args

    def execute_sub(self):
        if not self.__subparsers:
            return
        if hasattr(self.args, "sub_action"):
            self.args.sub_action(self.args)