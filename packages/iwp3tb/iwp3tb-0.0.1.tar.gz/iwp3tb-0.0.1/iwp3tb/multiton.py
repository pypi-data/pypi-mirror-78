#!/usr/bin/env python3

"""A set of handy decorators for my beloved Singleton and Multiton design patterns.

Concept
-------

A multiton here is an abstract class, that has a finite number of 
implementations. Each implementation is instantiated just once and this
instance is made available as an attribute of the parent multiton 
class.

A singleton is basically a multiton that has only one implementation. 
Thus no need to separate the abstract class from private 
implementation.

This approach allows for very private implementations while 
only the common interface becomes public.

Examples
--------

### Basic Multiton

```python
from iwp3tb import multiton, implementation

@multiton
class PowerRaiser():
    def raise_to_power(self, x: float) -> float:
        # This is an abstract method.
        # Implementations should realise it.
        raise Exception('You should have implemented this!')

@implementation
class Second(PowerRaiser):
    def raise_to_power(self, x):
        return x * x

@implementation
class Third(PowerRaiser):
    def raise_to_power(self, x):
        return x * x * x

print(PowerRaiser.Second.raise_to_power(3))
# prints out:
# 9

print(PowerRaiser.Third.raise_to_power(3))
# prints out:
# 27
```

### Custom Multiton

Arbitrary instance names can be used.

```python
from iwp3tb import multiton, implementation_named

@multiton
class PowerRaiser():
    def raise_to_power(self, x: float) -> float:
        # This is an abstract method.
        # Implementations should realise it.
        raise Exception('You should have implemented this!')

@implementation_named('power2')
class Second(PowerRaiser):
    def raise_to_power(self, x):
        return x * x

@implementation_named('power3')
class Third(PowerRaiser):
    def raise_to_power(self, x):
        return x * x * x

print(PowerRaiser.power2.raise_to_power(3))
# prints out:
# 9

print(PowerRaiser.power3.raise_to_power(3))
# prints out:
# 27
```

### Singleton

```python
from iwp3tb import singleton

@singleton
class Squarer():
    def to_square(self, x: float) -> float:
        return x * x

print(Squarer.instance.to_square(3))
# prints out:
# 9
```
"""

from iwp3tb import Ancestors

_REGISTRAR_ATTR = '_registrar_injection'
_SINGLETON_NAME = 'instance'

class MultitonError(Exception):
    """
    Common base class for multiton fatal errors.
    """

    def __init__(self, a_string):
        super().__init__(a_string)

class NoRegistrarParent(MultitonError):
    """
    An error raised if a class is decorated as an implementation but it has no 
    multiton parent.

    ```python
    from iwp3tb import implementation
    
    @implementation
    class BadImplementation():
        pass
    # Raises NoRegistrarParent
    ```
    """

    def __init__(self, a_class):
        super().__init__('No registrar parent found for %s' % str(a_class))

class AlreadyHasRegistrarParent(MultitonError):
    """
    An error raised if a class is decorated as an multiton but it already has a 
    multiton parent.

    ```python
    from iwp3tb import multiton
    
    @multiton
    class GoodMultiton():
        pass
    
    @multiton
    class BadMultiton(GoodMultiton):
        pass
    # Raises AlreadyHasRegistrarParent
    ```
    """

    def __init__(self, a_class, a_registrar):
        super().__init__('Class %s already has a registrar parent in %s' \
                         % (str(a_class), str(a_registrar)))

class RegistrarAlreadyHasAttribute(MultitonError):
    """
    An error raised if a naming conflict happens while registering an implementation 
    with a multiton.

    ```python
    from iwp3tb import multiton, implementation, implementation_named
    
    @multiton
    class GoodMultiton():
        pass
    
    @implementation
    class GoodImplementation(GoodMultiton):
        pass
    
    @implementation_named('GoodImplementation')
    class BadImplementation(GoodMultiton):
        pass
    # Raises RegistrarAlreadyHasAttribute
    ```
    """

    def __init__(self, a_class, a_registrar, a_name):
        super().__init__('Class %s can not be registered with registrar ' \
                         'parent %s since it already has attribute named %s ' \
                         % (str(a_class), str(a_registrar), a_name))

def _get_registrar(cls):
    found = None
    def _regHelper(c):
        nonlocal found
        found = getattr(c, _REGISTRAR_ATTR, None)
        return found is not None
    try:
        return next(found for c in Ancestors(cls) if _regHelper(c))
    except StopIteration:
        return None

def _register_as(cls, a_name):
    registrar = _get_registrar(cls)
    if registrar is None:
        raise NoRegistrarParent(cls) from None
    if hasattr(registrar, a_name):
        raise RegistrarAlreadyHasAttribute(cls, registrar, a_name) from None
    setattr(registrar, a_name, cls())
    return cls

def implementation(cls):
    """
    Class decorator that registers an implementation with a multiton 
    ancestor class. Class name is used for the implementation instance name. 
    The class name must not conflict with any of the multition attributes.
    """

    _register_as(cls, cls.__name__)

def implementation_named(a_name):
    """
    Class decorator that registers an implementation with a multiton 
    ancestor class using a custom instance name. The class name must not 
    conflict with any of the multition attributes.
    """

    return lambda cls: _register_as(cls, a_name)

def multiton(cls):
    """
    Class decorator for multiton. A multiton class should have no multition 
    or singleton ancestors.
    """

    registrar = _get_registrar(cls)
    if registrar is not None:
        raise AlreadyHasRegistrarParent(cls, registrar) from None
    setattr(cls, _REGISTRAR_ATTR, cls)
    return cls

def singleton(cls):
    """
    Class decorator for singleton. A singleton class should have no 
    multition or singleton ancestors.
    """

    _register_as(multiton(cls), _SINGLETON_NAME)
    return cls