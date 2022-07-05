"""Fibonacci sequence."""

from nspkg.subpkg.lucas import compute_lucas_u


def compute_fibonacci(n):
    """
    Compute element n of the Fibonacci sequence.

    This delegates to the lucas function in the module lucas module of this
    subpackage. That function takes exponential time, so this does too.
    """
    return compute_lucas_u(1, -1, n)