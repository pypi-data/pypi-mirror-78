#!/usr/bin/env python3

from iwp3tb import Ancestors

from .testpack.testmod import Tant
from .testpack.anotherpack.anothermod import Oma

import unittest

class Gran():
    def whoami(self):
        return self.__class__.__name__

class Dad(Gran):
    pass

class Mom(Oma):
    pass

class Son(Dad, Mom):
    pass

class HalfBro(Dad):
    pass

class Uncle(Gran):
    pass

class Niece(Uncle):
    pass

class TestAncestors(unittest.TestCase):
    def test_son(self):
        self.assertEqual(
            set(x.__name__ for x in Ancestors(Son)), 
            set(('Son', 'Dad', 'Gran', 'Mom', 'Oma')),
            )

    def test_Tant(self):
        self.assertEqual(
            set(x.__name__ for x in Ancestors(Tant)), 
            set(('Tant', 'Oma')),
            )

    def test_son_no_self(self):
        self.assertEqual(
            set(x.__name__ for x in Ancestors(Son, False)), 
            set(('Dad', 'Gran', 'Mom', 'Oma')),
            )

    def test_exhausted(self):
        a = Ancestors(Son)
        b = set(a)
        self.assertRaises(StopIteration, lambda: next(a))


