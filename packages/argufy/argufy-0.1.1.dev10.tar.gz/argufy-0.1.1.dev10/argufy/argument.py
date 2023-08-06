# -*- coding: utf-8 -*-
# copyright: (c) 2020 by Jesse Johnson.
# license: Apache 2.0, see LICENSE for more details.
'''Arguments for inspection based CLI parser.'''

import inspect
from ast import literal_eval
from typing import Any, Dict, Type

from docstring_parser.common import DocstringParam


class Argument:
    '''Represent argparse arguments.'''

    def __init__(
        self,
        parameters: Type[inspect.Parameter],
        docstring: Type[DocstringParam],
    ) -> None:
        '''Initialize argparse argument.'''
        self.attributes: Dict[Any, Any] = {}
        self.__docstring = docstring

        # Define attribute defaults
        self.nargs_type = '+'

        default = parameters.default
        name = parameters.name.replace('_', '-')
        if default == inspect._empty:  # type: ignore
            self.attributes['name'] = [name]
        else:
            self.attributes['name'] = ['--' + name]
            self.attributes['default'] = default

        self.set_attributes(self.get_annotations(parameters.annotation))
        if self.attributes['type'] != bool:
            self.attributes['metavar'] = (parameters.name).upper()
        if self.__docstring:
            self.attributes['help'] = self.__docstring.description

    # const
    # dest
    # required

    def get_annotations(self, annotation: Any) -> Any:
        '''Get parameter types for method/function.'''
        if annotation != inspect._empty:  # type: ignore
            return annotation
        elif self.__docstring and self.__docstring.type_name:
            annotation = literal_eval(self.__docstring.type_name)
            return annotation
        else:
            return None

    def set_attributes(self, annotation: Any) -> None:
        '''Define argument attributes.'''
        if type(annotation) == bool:
            # Note: these store type internally
            if self.attributes.get('default'):
                self.attributes['action'] = 'store_false'
            else:
                self.attributes['action'] = 'store_true'
        elif type(annotation) == int:
            self.attributes['type'] = annotation
            self.attributes['action'] = 'append'
        elif type(annotation) == list:
            self.attributes['type'] = annotation
            self.attributes['nargs'] = self.nargs_type
        elif type(annotation) == tuple:
            self.attributes['type'] = annotation[0]
            if type(annotation[1]) == set:
                self.attributes['choices'] = annotation[1]
        else:
            self.attributes['type'] = annotation
