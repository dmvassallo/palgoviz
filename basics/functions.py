#!/usr/bin/env python

"""
Examples demonstrating language features for functions.

This is a "bikeshed" file containing a handful of examples/exercises that don't
fit well elsewhere.

See also functions.ipynb, scopes.ipynb, and scopes.py.

Most material on higher-order functions is in composers.py or decorators.py.

TODO: Either move these functions to other modules or better explain what this
      module should and shouldn't contain.
"""

import itertools


def make_counter(start=0):
    """
    Create and return a function that returns successive integers on each call.

    This implementation never assigns to a variable that already exists.

    >>> f = make_counter()
    >>> [f(), f()]
    [0, 1]
    >>> g = make_counter()
    >>> [f(), g(), f(), g(), g()]
    [2, 0, 3, 1, 2]
    >>> h = make_counter(10)
    >>> [h(), f(), g(), h(), g(), h(), h(), g(), g(), f(), h()]
    [10, 4, 3, 11, 4, 12, 13, 5, 6, 5, 14]
    """
    it = itertools.count(start)
    return lambda: next(it)


def make_counter_alt(start=0):
    """
    Create and return a function that returns successive integers on each call.

    This implementation does not involve iterators in any way.

    >>> f = make_counter_alt()
    >>> [f(), f()]
    [0, 1]
    >>> g = make_counter_alt()
    >>> [f(), g(), f(), g(), g()]
    [2, 0, 3, 1, 2]
    >>> h = make_counter_alt(10)
    >>> [h(), f(), g(), h(), g(), h(), h(), g(), g(), f(), h()]
    [10, 4, 3, 11, 4, 12, 13, 5, 6, 5, 14]
    """
    previous = start - 1

    def counter():
        nonlocal previous
        previous += 1
        return previous

    return counter


def make_next_fibonacci():
    """
    Create and return a function that returns successive Fibonacci numbers on
    each call.

    This implementation is simple, using an existing function in the project.

    >>> f = make_next_fibonacci()
    >>> [f() for _ in range(5)]
    [0, 1, 1, 2, 3]
    >>> g = make_next_fibonacci()
    >>> [x for _ in range(5) for x in (g(), f())]
    [0, 5, 1, 8, 1, 13, 2, 21, 3, 34]
    >>> [f(), f(), g()]
    [55, 89, 5]
    """
    ...  # FIXME: Implement this.


def make_next_fibonacci_alt():
    """
    Create and return a function that returns successive Fibonacci numbers on
    each call.

    This implementation is self-contained: it does not use anything defined
    outside, not even builtins. It also does not involve iterators in any way.

    >>> f = make_next_fibonacci_alt()
    >>> [f() for _ in range(5)]
    [0, 1, 1, 2, 3]
    >>> g = make_next_fibonacci_alt()
    >>> [x for _ in range(5) for x in (g(), f())]
    [0, 5, 1, 8, 1, 13, 2, 21, 3, 34]
    >>> [f(), f(), g()]
    [55, 89, 5]
    """
    ...  # FIXME: Implement this.


def as_func(iterable):
    """
    Given an iterable, return a function that steps through it on each call.

    >>> f = as_func([10, 20, 30])
    >>> f()
    10
    >>> f()
    20
    >>> import itertools
    >>> g = as_func(x**2 for x in itertools.count(2))
    >>> f()
    30
    >>> g()
    4
    >>> f()
    Traceback (most recent call last):
      ...
    StopIteration
    >>> g()
    9
    >>> g()
    16
    """
    ...  # FIXME: Implement this.


def as_iterator_limited(func, end_sentinel):
    """
    Given a parameterless function, return an iterator that calls it until
    end_sentinel is reached.

    >>> it = as_iterator_limited(make_counter_alt(), 2000)
    >>> list(it) == list(range(2000))
    True
    >>> list(as_iterator_limited(make_next_fibonacci_alt(), 89))
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    """
    ...  # FIXME: Implement this.


def as_iterator_limited_alt(func, end_sentinel):
    """
    Given a parameterless function, return an iterator that calls it until
    end_sentinel is reached.

    This is an alternative implementation of as_iterator_limited. One
    implementation uses the iter builtin; the other does not.

    >>> it = as_iterator_limited_alt(make_counter_alt(), 2000)
    >>> list(it) == list(range(2000))
    True
    >>> list(as_iterator_limited_alt(make_next_fibonacci_alt(), 89))
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    """
    ...  # FIXME: Implement this.


def as_iterator(func):
    """
    Given a parameterless function, return an iterator that repeatedly calls
    it.

    >>> from itertools import islice
    >>> it = islice(as_iterator(make_counter_alt()), 2000)
    >>> list(it) == list(range(2000))
    True
    >>> list(islice(as_iterator(make_next_fibonacci_alt()), 11))
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    """
    ...  # FIXME: Implement this.


def as_iterator_alt(func):
    """
    Given a parameterless function, return an iterator that repeatedly calls
    it.

    This is an alternative implementation of as_iterator. One implementation
    uses the iter builtin; the other does not.

    >>> from itertools import islice
    >>> it = islice(as_iterator_alt(make_counter_alt()), 2000)
    >>> list(it) == list(range(2000))
    True
    >>> list(islice(as_iterator_alt(make_next_fibonacci_alt()), 11))
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    """
    ...  # FIXME: Implement this.


def count_tree_nodes(root):
    """
    Recursively count nodes in a tuple structure.

    Empty tuples and non-tuples are leaves. Other objects are internal nodes.
    The structure is treated as a tree: objects reached in more than one way
    are counted multiple times. No memoization is performed.

    This is a simple recursive implementation. No helper function is used.

    >>> count_tree_nodes('a parrot')
    1
    >>> count_tree_nodes(())
    1
    >>> a = ((2, 7, 1), (8, 6), (9, (4, 5)), ((((5, 4), 3), 2), 1))
    >>> count_tree_nodes(a)
    22
    >>> count_tree_nodes([a])
    1
    >>> from fibonacci import fib_nest
    >>> [count_tree_nodes(fib_nest(k)) for k in range(17)]
    [1, 1, 3, 5, 9, 15, 25, 41, 67, 109, 177, 287, 465, 753, 1219, 1973, 3193]
    """
    ...  # FIXME: Implement this.


def count_tree_nodes_alt(root):
    """
    Recursively count nodes in a tuple structure.

    Empty tuples and non-tuples are leaves. Other objects are internal nodes.
    The structure is treated as a tree: objects reached in more than one way
    are counted multiple times. No memoization is performed.

    This alternative implementation defines and calls a recursive helper
    function that does not return a value (really, it always returns None).
    No other callables, besides the helper and maybe builtins, are ever used.
    count_tree_nodes_alt never calls itself, nor does the helper ever call it.

    >>> count_tree_nodes_alt('a parrot')
    1
    >>> count_tree_nodes_alt(())
    1
    >>> a = ((2, 7, 1), (8, 6), (9, (4, 5)), ((((5, 4), 3), 2), 1))
    >>> count_tree_nodes_alt(a)
    22
    >>> count_tree_nodes_alt([a])
    1
    >>> from fibonacci import fib_nest
    >>> [count_tree_nodes_alt(fib_nest(k)) for k in range(17)]
    [1, 1, 3, 5, 9, 15, 25, 41, 67, 109, 177, 287, 465, 753, 1219, 1973, 3193]
    """
    ...  # FIXME: Implement this.


def count_tree_nodes_instrumented(root):
    """
    Call count_tree_nodes as if it were decorated with @decorators.peek_return.

    No logic from count_tree_nodes is reproduced. Subsequent calls to it do not
    have the modified behavior even if a prior call to it through this function
    raised an exception. But concurrent calls--like if it's called on another
    thread before a call to it through this function returns--need not be safe.

    Likewise, no logic from @peek_return is reproduced. If its behavior were to
    change--for example by using a different output format or even giving it by
    an entirely different means, such as posting it to a network server--then
    tests would need to change, but this function's implementation would not.

    >>> from recursion import make_deep_tuple
    >>> count_tree_nodes_instrumented(make_deep_tuple(2))
    count_tree_nodes(()) -> 1
    count_tree_nodes(((),)) -> 2
    count_tree_nodes((((),),)) -> 3
    3
    >>> count_tree_nodes(make_deep_tuple(3))
    4
    >>> try:
    ...     count_tree_nodes_instrumented(make_deep_tuple(5000))
    ... except RecursionError:
    ...     print('Got RecursionError.')
    ...     a = ((2, 7, 1), (8, 6), (9, (4, 5)), ((((5, 4), 3), 2), 1))
    ...     print(count_tree_nodes(a))
    Got RecursionError.
    22
    >>> from fibonacci import fib_nest
    >>> count_tree_nodes_instrumented(fib_nest(3))
    count_tree_nodes(1) -> 1
    count_tree_nodes(0) -> 1
    count_tree_nodes(1) -> 1
    count_tree_nodes((0, 1)) -> 3
    count_tree_nodes((1, (0, 1))) -> 5
    5
    """
    ...  # FIXME: Implement this.


if __name__ == '__main__':
    import doctest
    doctest.testmod()
