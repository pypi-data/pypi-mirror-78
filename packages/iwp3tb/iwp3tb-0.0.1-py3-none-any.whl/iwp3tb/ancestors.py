#!/usr/bin/env python3

"""A handy iterator through a class' custom ancestors.

Example
-------
```python
from iwp3tb import Ancestors

from andere.plek import Oma

class Gran():
    pass

class Dad(Gran):
    pass

class Mom(Oma):
    pass

class Son(Dad, Mom):
    pass

for cls in Ancestors(Son):
    print(cls.__name__)

# prints out:
# Son
# Dad
# Gran
# Mom
# Oma
```
"""

from typing import Iterator, Iterable


class Ancestors():
    """
    An iterator for non-builtin ancestors of a class

    Goes recursively through all custom (i.e. not builtin) classes that
    the base class inherits from. The base class itself comes first in the 
    iteration otherwise the order is unpredictable. Pass False as a second 
    argument to the constructor to avoid including the base class in the 
    iteration.
    """

    _BUILTINS: str = object.__class__.__module__


    def __init__(self, a_class: type, a_include_self: bool=True):
        """
        Parameters
        ----------
        a_class : type
            The base class, who's ancestors we want to iterate through
        a_include_self : bool, optional
            If True the base class itself is included in the iteration, 
            otherwise immedeatly proceeds to base class' ancestors. Defaults 
            to True
        """

        self.base_class: type = a_class
        self.current: type = None
        self.pool: Iterator[type] = (Ancestors(c) for c in a_class.__bases__ if c.__module__ != Ancestors._BUILTINS)
        self._next_worker: method = self._next_base_class if a_include_self \
                                                          else self._next_from_pool


    def __iter__(self) -> Iterable:
        return self


    def __next__(self) -> type:
        """
        Iterator interface method adapter
        """

        return self._next_worker()


    def _next_base_class(self) -> type:
        """
        Iterator's __next__ implementatation that returns the base class and
        passes the baton to another implementation.
        """

        self._next_worker = self._next_from_pool
        return self.base_class


    def _next_exhausted(self):
        """
        Terminal implementation of the Iterator's __next__ method.
        """

        raise StopIteration() from None


    def _next_from_pool(self) -> type:
        """
        Iterator's __next__ implementatation that goes through the pool of the
        pool of the base class' ancestors and replaces it self with another 
        implementation once the pool is exhausted.
        """

        if self.current is None:
            try:
                self.current = next(self.pool)
            except StopIteration:
                self._next_worker = self._next_exhausted
                self._next_exhausted()
        try:
            return next(self.current)
        except StopIteration:
            self.current = None
            return self.__next__()