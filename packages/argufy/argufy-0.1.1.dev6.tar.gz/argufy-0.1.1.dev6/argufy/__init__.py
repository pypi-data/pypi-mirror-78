# -*- coding: utf-8 -*-
# :copyright: (c) 2020 by Jesse Johnson.
# :license: Apache 2.0, see LICENSE for more details.
'''Inspection based parser based on argparse.'''

import logging
from typing import List

from .argument import Argument  # noqa
from .parser import Parser  # noqa

__all__: List[str] = ['Parser']

logging.getLogger(__name__).addHandler(logging.NullHandler())
