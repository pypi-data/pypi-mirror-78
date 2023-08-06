#!/usr/bin/env python3

"""Ish West Python 3 Toolbox is a random collection of handy tools.

## Exports
### Class ancestors iterator
* `ancestors.Ancestors`
### Decorators for singletons and multitons
* `multiton.singleton`
* `multiton.multiton`
* `multiton.implementation`
* `multiton.implementation_named`
"""

from .ancestors import Ancestors
from .multiton import multiton, implementation, implementation_named, singleton, MultitonError