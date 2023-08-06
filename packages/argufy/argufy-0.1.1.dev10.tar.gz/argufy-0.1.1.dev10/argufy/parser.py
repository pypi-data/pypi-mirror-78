# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Argufier is an inspection based CLI parser.'''

import inspect
import sys
from argparse import ArgumentParser
from types import ModuleType
from typing import Any, Callable, Optional, Sequence, Type, TypeVar

# from argparse_color_formatter import ColorHelpFormatter, ColorTextWrapper
from docstring_parser import parse

from .argument import Argument

# Define function as parameters for MyPy
F = TypeVar('F', bound=Callable[..., Any])

__exclude_prefixes__ = ('@', '_')


class Parser(ArgumentParser):
    '''Provide CLI parser for function.'''

    def __init__(self, *args: str, **kwargs: str) -> None:
        '''Initialize parser.

        Parameters
        ----------
        prog: str
            The name of the program
        usage: str
            The string describing the program usage
        description: str
            Text to display before the argument help
        epilog: str
            Text to display after the argument help
        parents: list
            A list of ArgumentParser objects whose arguments should also
            be included
        formatter_class: Object
            A class for customizing the help output
        prefix_chars: char
            The set of characters that prefix optional arguments
        fromfile_prefix_chars: None
            The set of characters that prefix files from which additional
            arguments should be read
        argument_default: None
            The global default value for arguments
        conflict_handler: Object
            The strategy for resolving conflicting optionals
        add_help: str
            Add a -h/--help option to the parser
        allow_abbrev: bool
            Allows long options to be abbreviated if the abbreviation is
            unambiguous

        '''
        if 'version' in kwargs:
            self.version = kwargs.pop('version')

        module = self.__get_parent_module()
        if module:
            docstring = parse(module.__doc__)
            if not kwargs.get('description'):
                kwargs['description'] = docstring.short_description

        super().__init__(**kwargs)  # type: ignore
        if not hasattr(self, 'subcommands'):
            self._subcommands = {}

        # if module:
        #     self._load_module(module)

    @staticmethod
    def __get_parent_module():
        module = None
        stack = inspect.stack()
        stack_frame = stack[1]

        # TODO: subparsers should have the same capability later
        if stack_frame.function != 'add_parser':
            module = inspect.getmodule(stack_frame[0])
        return module

    def add_arguments(
        self, obj: Any, parser: Optional[Type[ArgumentParser]] = None
    ) -> None:
        '''Add arguments to parser/subparser.'''
        if not parser:
            parser = self  # type: ignore
        docstring = parse(obj.__doc__)
        signature = inspect.signature(obj)
        for arg in signature.parameters:
            description = next(
                (d for d in docstring.params if d.arg_name == arg), None
            )
            argument = Argument(
                signature.parameters[arg], description  # type: ignore
            )
            # print('sig:', signature.parameters[arg])
            name = argument.attributes.pop('name')
            parser.add_argument(*name, **argument.attributes)  # type: ignore
        return self

    def add_commands(
        self,
        module: ModuleType,
        parser: Optional[Type[ArgumentParser]] = None,
        exclude_prefix: list = ['@', '_'],
    ) -> None:
        '''Add commands.'''
        if not parser:
            parser = self  # type: ignore
        module_name = module.__name__.split('.')[-1]
        docstring = parse(module.__doc__)
        parameters = {}

        command_parser = parser.add_subparsers(dest=module_name)
        # self._load_module(module, command_parser, exclude_prefix)
        for name, value in inspect.getmembers(module):
            # TODO: Possible singledispatch candidate
            if not name.startswith(__exclude_prefixes__):
                if inspect.isclass(value):
                    continue
                elif inspect.isfunction(value) or inspect.ismethod(value):
                    if (
                        module.__name__ == value.__module__
                        and not name.startswith(
                            (', '.join(__exclude_prefixes__))
                        )
                    ):
                        cmd = command_parser.add_parser(
                            name.replace('_', '-'),
                            help=docstring.short_description,
                        )
                        cmd.set_defaults(fn=value)
                        self.add_arguments(value, cmd)
                elif isinstance(value, (float, int, str, list, dict, tuple)):
                    parameters['default'] = getattr(module, name)
                    description = next(
                        (
                            d.description
                            for d in docstring.params
                            if d.arg_name == name
                        ),
                        None,
                    )
                    # print(name, parameters, description)
                    # argument = Argument(parameters, description)
                    parser.add_argument(
                        '--' + name.replace('_', '-'), help=description
                    )
        return self

    def add_subcommands(
        self,
        module: ModuleType,
        parser: Optional[Type[ArgumentParser]] = None,
        exclude_prefix: list = ['@', '_'],
    ) -> None:
        '''Add subcommands.'''
        if not parser:
            parser = self  # type: ignore
        module_name = module.__name__.split('.')[-1]
        docstring = parse(module.__doc__)

        command_parser = parser.add_subparsers(dest=module.__name__)
        subcommand_parser = command_parser.add_parser(
            module_name.replace('_', '-'), help=docstring.short_description,
        )
        subcommand_parser.set_defaults(mod=module)
        self.add_commands(module, subcommand_parser)
        return self

    def __set_module_arguments(self, fn, ns):
        '''Separe module arguments from functions.'''
        if 'mod' in ns:
            mod = vars(ns).pop('mod')
        else:
            mod = None
        signature = inspect.signature(fn)
        # Separate namespace from other variables
        args = [
            {k: vars(ns).pop(k)}
            for k in list(vars(ns).keys()).copy()
            if not signature.parameters.get(k)
        ]
        print(args)
        if mod:
            for arg in args:
                for k, v in arg.items():
                    mod.__dict__[k] = v
        return ns

    def retrieve(
        self, args: Sequence[str] = None, ns: Optional[str] = None,
    ) -> Callable[[F], F]:
        '''Retrieve values from CLI.'''
        main_ns, main_args = self.parse_known_args(args, ns)
        if main_args == [] and 'fn' in vars(main_ns):
            return main_args, main_ns
        else:
            if 'mod' in vars(main_ns):
                a = []
                a.append(vars(main_ns)['mod'].__name__.split('.')[-1])
                a.append('--help')
            self.parse_args(a)

    def dispatch(
        self, args: Sequence[str] = None, ns: Optional[str] = None,
    ) -> Callable[[F], F]:
        '''Call command with arguments.'''
        if sys.argv[1:] == [] and args is None:
            args = ['--help']
        arguments, namespace = self.retrieve(args, ns)
        if 'fn' in namespace:
            fn = vars(namespace).pop('fn')
            namespace = self.__set_module_arguments(fn, namespace)
            return fn(**vars(namespace))
