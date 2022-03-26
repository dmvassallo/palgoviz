"""Some simple code, for unit testing."""

import sys
from abc import ABC, abstractmethod
import enum
import functools

MY_NONE = None


class Widget:
    """Something with size and color attributes, disallowing new attributes."""

    __slots__ = ('size', 'color')

    def __init__(self, size, color):
        """Create a new widget of the specified size and color."""
        self.size = size
        self.color = color


def answer():
    """
    Return the int said to answer the question of life/the universe/everything.
    """
    return 42


def is_sorted(items):
    """Check if an iterable is sorted."""
    my_items = list(items)
    return my_items == sorted(my_items)


def alert(message):
    """Print an alert to standard error, with a simple "alert:" prefix."""
    print(f'alert: {message}', file=sys.stderr)


def bail_if(condition):
    """Exit indicating failure if the condition evaluates as true."""
    if condition: sys.exit(1)


class Squarer(ABC):
    """Abstract class representing squarers."""

    __slots__ = ()

    @abstractmethod
    def __call__(self, number):
        """Square a number."""
        ...

    def __repr__(self):
        """Represent this Squarer as Python code."""
        return f"{type(self).__name__}()"

    def __eq__(self, other):
        """Check if two Squarers are of the same type."""
        if not isinstance(other, Squarer):
            return NotImplemented
        return type(self) is type(other)

    def __hash__(self):
        return hash(type(self))


class MulSquarer(Squarer):
    """Callable object that squares numbers with the * operator."""

    __slots__ = ()

    def __call__(self, number):
        """
        Square a number using the * operator.

        >>> m = MulSquarer()
        >>> m(3)
        9
        """
        return number * number


class PowSquarer(Squarer):
    """Callable object that squares numbers with the ** operator."""

    __slots__ = ()

    def __call__(self, number):
        """
        Square a number using the ** operator.

        >>> p = PowSquarer()
        >>> p(3)
        9
        """
        return number**2


def make_squarer():
    """
    Return a function that squares.

    >>> f = make_squarer()
    >>> f(3)
    9
    """
    return lambda x: x**2


def _ensure_toggle_start_bool(start):
    """Helper for Toggle and make_toggle. Ensure start is the correct type."""
    if not isinstance(start, bool):
        raise TypeError(f'start must be bool, got {type(start).__name__}')


class Toggle:
    """
    Callable object returning alternating bools.

    >>> tf = Toggle(True)
    >>> tf()
    True
    >>> tf()
    False
    >>> tf()
    True
    >>> ft = Toggle(False)
    >>> ft()
    False
    >>> ft()
    True
    >>> ft()
    False
    """

    __slots__ = ('_value',)

    def __init__(self, start):
        """Make a Toggle that will return the given value when first called."""
        _ensure_toggle_start_bool(start)
        self._value = start

    def __repr__(self):
        """eval-able representation of this Toggle."""
        return f'{type(self).__name__}({self._value!r})'

    def __eq__(self, other):
        """Toggles are equal when they would return the same bool if called."""
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._value is other._value

    def __call__(self):
        """Return a bool different from what the next call will return."""
        ret = self._value
        self._value = not ret
        return ret


def make_toggle(start):
    """
    Create a function that returns alternating bools.

    >>> tf = make_toggle(True)
    >>> tf()
    True
    >>> tf()
    False
    >>> tf()
    True
    >>> ft = make_toggle(False)
    >>> ft()
    False
    >>> ft()
    True
    >>> ft()
    False
    """
    _ensure_toggle_start_bool(start)

    def toggle():
        nonlocal start
        ret = start
        start = not start
        return ret

    return toggle


@functools.total_ordering
@enum.unique
class BearBowl(enum.Enum):
    """
    A bowl of porridge Goldilocks tasted while trespassing in a bear kitchen.

    BearBowls compare by heat: a cooler bowl is less than a warmer bowl.

    >>> BearBowl.TOO_COLD < BearBowl.JUST_RIGHT < BearBowl.TOO_HOT
    True
    """

    TOO_COLD = 1
    JUST_RIGHT = 2
    TOO_HOT = 3

    def __repr__(self):
        """eval-able representation (attribute-access expression)."""
        return str(self)

    def __lt__(self, other):
        """Compare by heat. Cooler bowls compare less than warmer bowls."""
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.value < other.value
