#!/usr/bin/env python3
# vim: set filetype=python sts=4 ts=4 sw=4 expandtab tw=100 cc=+1:
# vim: set filetype=python tw=100 cc=+1:
# pylint: disable=reimported,wrong-import-position
# pylint: disable=missing-docstring
# pylint: disable=bad-option-value,bad-continuation
# pylint: disable=ungrouped-imports
# pylint: disable=dangerous-default-value

# mypy: warn-unused-configs, disallow-any-generics, disallow-subclassing-any
# mypy: disallow-untyped-calls, disallow-untyped-defs, disallow-incomplete-defs
# mypy: check-untyped-defs, disallow-untyped-decorators, no-implicit-optional,
# mypy: warn-redundant-casts, warn-unused-ignores, warn-return-any, no-implicit-reexport,
# mypy: strict-equality

"""
This module is boilerplate for a python CLI script.
"""

# python3 -m pylint --rcfile=/dev/null boilerplate.py
# python3 -m mypy boilerplate.py

import logging
LOGGER = logging.getLogger(__name__)

import os.path
SCRIPT_DIRNAME = os.path.dirname(__file__)
SCRIPT_DIRNAMEABS = os.path.abspath(SCRIPT_DIRNAME)
SCRIPT_BASENAME = os.path.basename(__file__)

import pathlib
SCRIPT_PATH = pathlib.Path(__file__)

import sys
import argparse
import contextlib
import typing as typ
import inspect
import rdflib
import rdflib.plugins.sparql as rlsparql
import rdflib.namespace as rlns
import rdflib.util as rlutil
import owlrl
import yaml
import enum

GenericT = typ.TypeVar('GenericT')
def collate(*args: typ.Optional[GenericT]) -> typ.Optional[GenericT]:
    for arg in args:
        if arg is not None:
            return arg
    return None

def vdict(*keys: str, obj: typ.Any = None) -> typ.Dict[str, typ.Any]:
    if obj is None:
        lvars = typ.cast(typ.Any, inspect.currentframe()).f_back.f_locals
        return {key: lvars[key] for key in keys}
    return {key: getattr(obj, key, None) for key in keys}

def static_init(cls: typ.Any) -> typ.Any:
    if getattr(cls, "static_init", None):
        cls.static_init()
    return cls

@static_init
class ReasonerClosureClass(enum.Enum):
    key_strings: typ.ClassVar[typ.Set[str]]

    RDFS_Semantics = owlrl.CombinedClosure.RDFS_Semantics
    OWLRL_Semantics = owlrl.CombinedClosure.OWLRL_Semantics
    RDFS_OWLRL_Semantics = owlrl.CombinedClosure.RDFS_OWLRL_Semantics

    @classmethod
    def static_init(cls) -> None:
        setattr(cls, "key_strings", set())
        for enm in cls:
            cls.key_strings.add(enm.name) # type: ignore

    @classmethod
    def from_string(cls, string: str) -> owlrl.Closure.Core:
        if string not in cls.key_strings:  # type: ignore
            raise ValueError("Invalid closure class name {}. Must be one of {}"
                .format(string, ", ".join(cls.key_strings))) # type: ignore
        return cls[string].value

ArgsT = typ.List[str]
OptArgsT = typ.Optional[ArgsT]
OptParseResultT = typ.Optional[argparse.Namespace]
OptParserT = typ.Optional[argparse.ArgumentParser]
class Application:
    parser: argparse.ArgumentParser
    args: OptArgsT
    parse_result: OptParseResultT
    def __init__(self, parser: OptParserT = None):
        self.parse_result = None
        self.args = None
        self._do_init(parser)

    def _do_init(self, parser: OptParserT = None) -> None:
        if parser is None:
            own_parser = True
            self.parser = argparse.ArgumentParser(add_help=True)
        else:
            self.parser = parser
            own_parser = False
        parser = self.parser
        if own_parser:
            parser.add_argument("-v", "--verbose", action="count", dest="verbosity",
                help="increase verbosity level")
        parser.set_defaults(handler=self.handle)
        parsers: typ.List[argparse.ArgumentParser] = [parser]

        @contextlib.contextmanager
        def new_subparser(name: str, parser_args: typ.Dict[str, typ.Any] = {},
            subparsers_args: typ.Dict[str, typ.Any] = {}) \
            -> typ.Generator[argparse.ArgumentParser, None, None]:
            parent_parser = parsers[-1]
            if not hasattr(parent_parser, '_xsubparsers'):
                setattr(parent_parser, '_xsubparsers',
                    parent_parser.add_subparsers(dest=f"subparser_{len(parsers)}",
                        **subparsers_args))
            parent_subparsers = getattr(parent_parser, '_xsubparsers')
            parsers.append(parent_subparsers.add_parser(name, **parser_args))
            try:
                yield parsers[-1]
            finally:
                parsers.pop()

        # owlrl.DeductiveClosure

        with new_subparser("reason") as subparser:
            subparser.set_defaults(handler=self.handle_reason)
            subparser.add_argument("--closure-class", "--cc", action="store",
                dest="reasoner_closure_class", type=str, default="RDFS_OWLRL_Semantics",
                help="File containing prefixes to use")
            subparser.add_argument("--options", "--opts", action="store",
                dest="reasoner_options", type=str,
                help="File containing prefixes to use")
            subparser.add_argument("--input-format", "--if", action="store",
                type=str,
                help="Input format to use")
            subparser.add_argument("--output-format", "--of", action="store",
                type=str, default="turtle",
                help="Input format to use")
            subparser.add_argument("data_file", action="append",
                type=str, nargs="+",
                help="File containing prefixes to use")

        with new_subparser("sparql") as subparser:
            subparser.set_defaults(handler=self.handle_sparql)
            group = subparser.add_mutually_exclusive_group(required=True)
            group.add_argument("--query", "-q", action="store",
                dest="query", type=str,
                help="The SPARQL query to run")
            group.add_argument("--query-file", "-Q", action="store",
                dest="query_file", type=str,
                help="Path to a file containing the SPARQL query to run")
            subparser.add_argument("--no-default-prefixes", "--no-dp", action="store_false",
                dest="default_prefixes", default=True,
                help="The SPARQL query to run")
            subparser.add_argument("--prefix", "-p", action="append",
                dest="prefixes", default=[],
                help="Define prefix")
            subparser.add_argument("--prefix-file", "-P", action="store",
                dest="prefix_file", type=str,
                help="File containing prefixes to use")
            subparser.add_argument("--reason", action="store_true",
                dest="reason", default=False,
                help="Enable reasoning")
            subparser.add_argument("--reasoner-closure-class", "--reason-cc", action="store",
                dest="reasoner_closure_class", type=str, default="RDFS_OWLRL_Semantics",
                help="File containing prefixes to use")
            subparser.add_argument("--reasoner-options", "--reason-opts", action="store",
                dest="reasoner_options", type=str,
                help="File containing prefixes to use")
            subparser.add_argument("--input-format", "--if", action="store",
                type=str,
                help="Input format to use")
            subparser.add_argument("--output-format", "--of", action="store",
                type=str, default="csv",
                help="Input format to use")
            subparser.add_argument("data_file", action="append",
                type=str, nargs="+",
                help="File containing prefixes to use")

    def _parse_args(self, args: OptArgsT = None) -> None:
        self.args = collate(args, self.args, sys.argv[1:])
        self.parse_result = self.parser.parse_args(self.args)

        verbosity = self.parse_result.verbosity
        if verbosity is not None:
            root_logger = logging.getLogger("")
            root_logger.propagate = True
            new_level = (root_logger.getEffectiveLevel() -
                (min(1, verbosity)) * 10 - min(max(0, verbosity - 1), 9) * 1)
            root_logger.setLevel(new_level)

        LOGGER.debug("args = %s, parse_result = %s, logging.level = %s, LOGGER.level = %s",
            self.args, self.parse_result, logging.getLogger("").getEffectiveLevel(),
            LOGGER.getEffectiveLevel())

        if "handler" in self.parse_result and self.parse_result.handler:
            self.parse_result.handler(self.parse_result)

    def do_invoke(self, args: OptArgsT = None) -> None:
        self._parse_args(args)

    # parser is so this can be nested as a subcommand ...
    @classmethod
    def invoke(cls, *, parser: OptParserT = None, args: OptArgsT = None) -> None:
        app = cls(parser)
        app.do_invoke(args)

    def handle(self, parse_result: OptParseResultT = None) -> None:
        LOGGER.debug("entry ...")
        self.parse_result = parse_result = collate(parse_result, self.parse_result)

    def handle_reason(self, parse_result: OptParseResultT = None) -> None:
        LOGGER.debug("entry ...")
        self.handle(parse_result)
        parse_result = self.parse_result
        assert parse_result

        graph = rdflib.Graph()
        data_files = parse_result.data_file[0]
        for data_file in data_files:
            fmt = rdflib.util.guess_format(data_file)
            LOGGER.debug("Loading %s with format %s", data_file, fmt)
            graph.parse(source=data_file, format=parse_result.input_format)

        reasoner_options = parse_result.reasoner_options
        closure_class_name = parse_result.reasoner_closure_class
        closure_class = ReasonerClosureClass.from_string(closure_class_name)
        reasoner = owlrl.DeductiveClosure(closure_class, **yaml.safe_load(reasoner_options or "{}"))
        reasoner.expand(graph)
        sys.stdout.write(graph.serialize(format="turtle").decode("utf-8"))


    def handle_sparql(self, parse_result: OptParseResultT = None) -> None:
        LOGGER.debug("entry ...")
        self.handle(parse_result)
        parse_result = self.parse_result
        assert parse_result
        query_string = parse_result.query
        if query_string is None:
            query_string = pathlib.Path(parse_result.query_file).read_text()

        initNs = {
            "dc": rlns.DC,
            "dcterms": rlns.DCTERMS,
            "fn": rlns.Namespace("http://www.w3.org/2005/xpath-functions#"),
            "foaf": rlns.FOAF,
            "geo": rlns.Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#"),
            "owl": rlns.OWL,
            "rdf": rlns.RDF,
            "rdfs": rlns.RDFS,
            "sfn": rlns.Namespace("http://www.w3.org/ns/sparql#"),
            "skos": rlns.SKOS,
            "vann": rlns.Namespace("http://purl.org/vocab/vann/"),
            "xml": rlns.Namespace("http://www.w3.org/XML/1998/namespace#"),
            "xsd": rlns.XSD,
            "cc": rlns.Namespace("http://creativecommons.org/ns#"),
        }

        query = rlsparql.prepareQuery(query_string, initNs=initNs)

        graph = rdflib.Graph()
        data_files = parse_result.data_file[0]
        for data_file in data_files:
            fmt = rdflib.util.guess_format(data_file)
            LOGGER.debug("Loading %s with format %s", data_file, fmt)
            graph.parse(source=data_file, format=parse_result.input_format)


        if parse_result.reason:
            reasoner_options = parse_result.reasoner_options
            closure_class_name = parse_result.reasoner_closure_class
            closure_class = ReasonerClosureClass.from_string(closure_class_name)
            reasoner = owlrl.DeductiveClosure(closure_class, **yaml.safe_load(reasoner_options or "{}"))
            reasoner.expand(graph)

        query_result = graph.query(query)
        LOGGER.debug(vdict('query_result'))
        sys.stdout.buffer.write(query_result.serialize(format=parse_result.output_format))



def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stderr,
        datefmt="%Y-%m-%dT%H:%M:%S",
        format=("%(asctime)s %(process)d %(thread)d %(levelno)03d:%(levelname)-8s "
            "%(name)-12s %(module)s:%(lineno)s:%(funcName)s %(message)s"))

    Application.invoke()

if __name__ == "__main__":
    main()
