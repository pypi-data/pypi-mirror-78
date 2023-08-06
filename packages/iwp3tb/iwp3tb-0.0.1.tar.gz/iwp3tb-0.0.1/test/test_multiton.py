#!/usr/bin/env python3

from iwp3tb import multiton, implementation, implementation_named, singleton, MultitonError

from .testpack.testmod import Tant
from .testpack.anotherpack.anothermod import Oma

import unittest

@multiton
class Gran():
    def whoami(self):
        return self.__class__.__name__

class Dad(Gran):
    pass

class Mom(Oma):
    pass

@implementation
class Son(Dad, Mom):
    pass

@implementation_named('DumbBro')
class HalfBro(Dad):
    pass

class Uncle(Gran):
    pass

@implementation
class Niece(Uncle):
    pass

@singleton
class Orphan():
    pass

class Imposter(Gran):
    pass

class TestRegistrations(unittest.TestCase):

    # Test multiton

    def test_son(self):
        self.assertEqual(
            Gran.Son.whoami(), 
            'Son',
            )

    def test_half_bro(self):
        self.assertEqual(
            Gran.DumbBro.whoami(), 
            'HalfBro',
            )

    def test_niece(self):
        self.assertEqual(
            Gran.Niece.whoami(), 
            'Niece',
            )

    # Test singleton

    def test_singleton(self):
        self.assertEqual(
            Orphan.instance.__class__.__name__,
            'Orphan',
            )

    # Test errors

    def test_no_registrar(self):
        self.assertRaises(MultitonError, lambda: implementation(Mom))

    def test_already_has_registrar(self):
        self.assertRaises(MultitonError, lambda: multiton(Dad))

    def test_already_has_attribute(self):
        self.assertRaises(MultitonError, lambda: implementation_named('DumbBro')(Imposter))

