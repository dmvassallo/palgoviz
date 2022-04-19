#!/usr/bin/env python

"""Tests for the types in compare.py."""

import copy
from fractions import Fraction
import pickle
import unittest

from parameterized import parameterized

from compare import OrderIndistinct, Patient, WeakDiamond


class TestWeakDiamond(unittest.TestCase):
    """Tests for the WeakDiamond class."""

    @parameterized.expand(['NORTH', 'SOUTH', 'EAST', 'WEST'])
    def test_equal(self, name):
        """Equality comparisons work in the usual way for enumerations."""
        lhs = getattr(WeakDiamond, name)
        rhs = getattr(WeakDiamond, name)
        self.assertEqual(lhs, rhs)

    @parameterized.expand([
        ('NORTH, SOUTH', 'NORTH', 'SOUTH'),
        ('NORTH, EAST', 'NORTH', 'EAST'),
        ('NORTH, WEST', 'NORTH', 'WEST'),
        ('SOUTH, EAST', 'SOUTH', 'EAST'),
        ('SOUTH, WEST', 'SOUTH', 'WEST'),
        ('EAST, WEST', 'EAST', 'WEST'),
    ])
    def test_not_equal(self, _label, name1, name2):
        """Not-equals comparisons work in the usual way for enumerations."""
        for lhs_name, rhs_name in (name1, name2), (name2, name1):
            with self.subTest(lhs=lhs_name, rhs=rhs_name):
                lhs_comparand = getattr(WeakDiamond, lhs_name)
                rhs_comparand = getattr(WeakDiamond, rhs_name)
                self.assertNotEqual(lhs_comparand, rhs_comparand)

    @parameterized.expand([
        ('SOUTH, NORTH', 'SOUTH', 'NORTH'),
        ('SOUTH, EAST', 'SOUTH', 'EAST'),
        ('SOUTH, WEST', 'SOUTH', 'WEST'),
        ('EAST, NORTH', 'EAST', 'NORTH'),
        ('WEST, NORTH', 'WEST', 'NORTH'),
    ])
    def test_souther_less_than_norther(self, _label, lhs_name, rhs_name):
        """Farther south directions compare less than farther north ones."""
        lhs_comparand = getattr(WeakDiamond, lhs_name)
        rhs_comparand = getattr(WeakDiamond, rhs_name)
        self.assertLess(lhs_comparand, rhs_comparand)


    def test_souther_less_equal_norther_or_same(self, _label,
                                                lhs_name, rhs_name):
        """Directions are "<=" when they are "<" or they are "=="."""
        ('SOUTH, NORTH', 'SOUTH', 'NORTH'),
        ('SOUTH, SOUTH', 'SOUTH', 'NORTH'),
        ('SOUTH, EAST', 'SOUTH', 'EAST'),
        ('SOUTH, WEST', 'SOUTH', 'WEST'),
        ('EAST, EAST', 'EAST', 'NORTH'),
        ('EAST, NORTH', 'EAST', 'NORTH'),
        ('WEST, WEST', 'WEST', 'NORTH'),
        ('WEST, NORTH', 'WEST', 'NORTH'),

    @parameterized.expand([
        ('NORTH, EAST', 'NORTH', 'EAST'),
        ('NORTH, WEST', 'NORTH', 'WEST'),
        ('NORTH, SOUTH', 'NORTH', 'SOUTH'),
        ('EAST, SOUTH', 'EAST', 'SOUTH'),
        ('WEST, SOUTH', 'WEST', 'SOUTH'),
    ])
    def test_norther_greater_than_souther(self, _label, lhs_name, rhs_name):
        """Farther north directions compare greater than farther south ones."""
        lhs_comparand = getattr(WeakDiamond, lhs_name)
        rhs_comparand = getattr(WeakDiamond, rhs_name)
        self.assertGreater(lhs_comparand, rhs_comparand)

    # def test_north_greater_than_south(self):
    #    self.assertTrue(WeakDiamond.NORTH > WeakDiamond.SOUTH)


class TestPatient(unittest.TestCase):
    """Tests for the Patient class."""


class TestOrderIndistinct(unittest.TestCase):
    """
    Tests for the OrderIndistinct class.

    TODO: Once bobcats.py and test_bobcats.py are merged in, make note of
    design and style differences between this and the test_bobcats tests.
    """

    _VALUE_ARGS_WITHOUT_JUST_OBJ = [
        ('int', 42),
        ('str', 'ham'),
        ('list of str', ['foo', 'bar', 'baz', 'quux', 'foobar']),
        ('list of int', [10, 20, 30, 40, 50, 60, 70]),
        ('Fraction', Fraction(5, 9)),
        ('None', None),
    ]
    """Labeled values of, or containing, different types; but not object()."""

    _VALUE_ARGS = _VALUE_ARGS_WITHOUT_JUST_OBJ + [('just obj', object())]
    """Some labeled values of, or containing, different types."""

    _VALUE_ARGS_WITH_EXPECTED_REPR = [
        ('int', 42, 'OrderIndistinct(42)'),
        ('str', 'ham', "OrderIndistinct('ham')"),
        ('list of str',
        ['foo', 'bar', 'baz', 'quux', 'foobar'],
        "OrderIndistinct(['foo', 'bar', 'baz', 'quux', 'foobar'])"),
        ('list of int',
        [10, 20, 30, 40, 50, 60, 70],
        "OrderIndistinct([10, 20, 30, 40, 50, 60, 70])"),
        ('Fraction', Fraction(5, 9), 'OrderIndistinct(Fraction(5, 9))'),
        ('None', None, 'OrderIndistinct(None)'),
    ]
    """Labeled values and expected OrderIndistinct object reprs."""

    _DISTINCT_VALUE_PAIRS = [
        ('ints', 42, 76),
        ('strs', 'ham', 'foo'),
        ('lists of str', ['foo', 'bar'], ['foo', 'baz']),
        ('lists of int', [1, 2, 3, 4, 5], [1, 3, 4, 3, 5]),
        ('singletons', None, ...),
        ('just objs', object(), object()),
    ]
    """Labeled pairs of distinct values of, and containing, the same type."""

    _VALUE_SEQUENCES = [
        ('letters', ['Y', 'X', 'C', 'A', 'E', 'B', 'D']),
        ('ints', [4, 9, 3, 7, 5, 15, 0, 18, 19, 11, 12, 16, 17, 14, 1, 13, 8]),
        ('str lists', [
            ['ham', 'spam', 'eggs'],
            ['foo', 'bar', 'baz', 'quux', 'foobar'],
            ['Alice', 'Bob', 'Carol', 'Cassidy', 'Christine', 'Derek'],
        ]),
        ('just objs', [object(), object(), object(), object(), object()]),
    ]
    """Labeled sequences of values, for testing stable sorting."""

    __slots__ = ()

    def test_cannot_construct_with_no_arguments(self):
        """Passing less than 1 argument to the constructor raises TypeError."""
        with self.assertRaises(TypeError):
            OrderIndistinct()

    def test_cannot_construct_with_multiple_arguments(self):
        """Passing more than 1 argument to the constructor raises TypeError."""
        with self.assertRaises(TypeError):
            OrderIndistinct(10, 20)

    @parameterized.expand(_VALUE_ARGS)
    def test_can_construct_with_single_argument(self, _label, value):
        """Passing a single argument to the constructor works."""
        try:
            OrderIndistinct(value)
        except TypeError as error:  # Makes TypeError "FAIL" (not "ERROR").
            description = 'TypeError calling OrderIndistinct with one argument'
            msg_info = f'(message: {error})'
            self.fail(f'{description} {msg_info}')

    @parameterized.expand(_VALUE_ARGS_WITH_EXPECTED_REPR)
    def test_repr_shows_type_with_value_arg(self, _label, value, expected):
        """The repr looks like code that could've created the object."""
        oi = OrderIndistinct(value)
        actual = repr(oi)
        self.assertEqual(actual, expected)

    @parameterized.expand(_VALUE_ARGS_WITHOUT_JUST_OBJ)
    def test_repr_roundtrips_by_eval(self, _label, value):
        """The repr is Python code that when eval'd gives an equal object."""
        original = OrderIndistinct(value)
        copy = eval(repr(original))
        self.assertEqual(original, copy)

    @parameterized.expand(_VALUE_ARGS_WITH_EXPECTED_REPR)
    def test_repr_correct_in_derived_class(self, _label, value, base_expected):
        """The repr shows a derived-class name (and also the correct value)."""
        class Derived(OrderIndistinct): pass
        derived_expected = base_expected.replace('OrderIndistinct', 'Derived')
        oi = Derived(value)
        actual = repr(oi)
        self.assertEqual(actual, derived_expected)

    @parameterized.expand(_VALUE_ARGS)
    def test_value_attr_has_original_value_arg(self, _label, value):
        """A positional argument on construction writes the value attribute."""
        oi = OrderIndistinct(value)
        self.assertEqual(oi.value, value)

    @parameterized.expand(_VALUE_ARGS)
    def test_value_attr_has_original_value_keyword_arg(self, _label, value):
        """A value= keyword arg on construction writes the value attribute."""
        oi = OrderIndistinct(value=value)
        self.assertEqual(oi.value, value)

    @parameterized.expand(_VALUE_ARGS)
    def test_value_attribute_can_be_changed(self, _label, new_value):
        """The value attribute is read-write. Reads see earlier writes."""
        old_value = object()
        oi = OrderIndistinct(old_value)
        oi.value = new_value
        with self.subTest(comparison='!= old'):
            self.assertNotEqual(oi.value, old_value)
        with self.subTest(comparison='== new'):
            self.assertEqual(oi.value, new_value)

    def test_new_attributes_cannot_be_created(self):
        """Assigning to a nonexistent attribute raises AttributeError."""
        oi = OrderIndistinct(42)
        with self.assertRaises(AttributeError):
            oi.valur = 76  # Misspelling of "value".

    @parameterized.expand(_VALUE_ARGS)
    def test_we_get_a_new_object_even_with_the_same_value(self, _label, value):
        """
        Calling OrderIndistinct always constructs a new object.

        This behavior is important because OrderIndistinct is a mutable type.
        """
        first = OrderIndistinct(value)
        second = OrderIndistinct(value)
        self.assertIsNot(first, second)

    @parameterized.expand(_VALUE_ARGS)
    def test_equal_when_value_is_equal(self, _label, value):
        """From the same value argument, OrderIndistint objects are equal."""
        # In unittest tests, we usually use assertEqual/assertNotEqual, rather
        # than writing the == and != operators with assertTrue/assertFalse.
        # However, when testing the == and != operators themselves, some people
        # like to write them explicitly. This can help test for unusual, but
        # possible, bugs, if both == and != are meant to use __eq__ but don't.
        first = OrderIndistinct(value)
        second = OrderIndistinct(value)
        with self.subTest(comparison='=='):
            self.assertTrue(first == second)
        with self.subTest(comparison='!='):
            self.assertFalse(first != second)

    @parameterized.expand(_DISTINCT_VALUE_PAIRS)
    def test_not_equal_when_value_is_not_equal(self, _label, lhs, rhs):
        """
        From different value arguments, OrderIndistinct objects are unequal.
        """
        # See the comment in test_equal_when_value_is_equal on this technique.
        first = OrderIndistinct(lhs)
        second = OrderIndistinct(rhs)
        with self.subTest(comparison='=='):
            self.assertFalse(first == second)
        with self.subTest(comparison='!='):
            self.assertTrue(first != second)

    @parameterized.expand(_VALUE_ARGS)
    def test_not_less_with_same_value(self, _label, value):
        """From the same value argument, "<" is false."""
        first = OrderIndistinct(value)
        second = OrderIndistinct(value)
        self.assertFalse(first < second)  # No assertNotLess method.

    @parameterized.expand(_DISTINCT_VALUE_PAIRS)
    def test_not_less_with_different_values(self, _label, lhs, rhs):
        """From different value arguments, "<" is false."""
        first = OrderIndistinct(lhs)
        second = OrderIndistinct(rhs)
        self.assertFalse(first < second)  # No assertNotLess method.

    @parameterized.expand(_VALUE_ARGS)
    def test_not_greater_with_same_value(self, _label, value):
        """From the same value argument, ">" is false."""
        first = OrderIndistinct(value)
        second = OrderIndistinct(value)
        self.assertFalse(first > second)  # No assertNotGreater method.

    @parameterized.expand(_DISTINCT_VALUE_PAIRS)
    def test_not_greater_with_different_values(self, _label, lhs, rhs):
        """From different value arguments, ">" is false."""
        first = OrderIndistinct(lhs)
        second = OrderIndistinct(rhs)
        self.assertFalse(first > second)  # No assertNotGreater method.

    @parameterized.expand(_VALUE_ARGS)
    def test_less_or_equal_with_same_value(self, _label, value):
        """From the same value argument, "<=" is true."""
        first = OrderIndistinct(value)
        second = OrderIndistinct(value)
        self.assertLessEqual(first, second)

    @parameterized.expand(_DISTINCT_VALUE_PAIRS)
    def test_not_less_or_equal_with_different_values(self, _label, lhs, rhs):
        """From different value arguments, "<=" is false."""
        first = OrderIndistinct(lhs)
        second = OrderIndistinct(rhs)
        self.assertFalse(first <= second)  # No assertNotLessEqual method.

    @parameterized.expand(_VALUE_ARGS)
    def test_greater_or_equal_with_same_value(self, _label, value):
        """With OrderIndistincts of the same value argument, ">=" is true."""
        first = OrderIndistinct(value)
        second = OrderIndistinct(value)
        self.assertGreaterEqual(first, second)

    @parameterized.expand(_DISTINCT_VALUE_PAIRS)
    def test_not_greater_or_equal_with_different_values(self,
                                                        _label, lhs, rhs):
        """From different value arguments, ">=" is false."""
        first = OrderIndistinct(lhs)
        second = OrderIndistinct(rhs)
        self.assertFalse(first >= second)  # No assertNotLessEqual method.

    def test_not_hashable(self):
        """
        Calling hash on an OrderIndistinct raises TypeError.

        This behavior is important because OrderIndistinct is a mutable type.
        """
        oi = OrderIndistinct(42)
        with self.assertRaises(TypeError):
            hash(oi)

    @parameterized.expand(_VALUE_SEQUENCES)
    def test_not_rearranged_by_sorted_builtin(self, _label, values):
        """sorted is stable, so it preserves OrderIndistinct objects' order."""
        before_sorting = [OrderIndistinct(x) for x in values]
        after_sorting = sorted(before_sorting)
        self.assertListEqual(before_sorting, after_sorting)

    @parameterized.expand(_VALUE_SEQUENCES)
    def test_not_rearranged_by_list_sort_method(self, _label, values):
        """
        list.sort is stable, so it preserves OrderIndistict objects' order.
        """
        original = [OrderIndistinct(x) for x in values]
        copy = original[:]
        copy.sort()
        self.assertListEqual(original, copy)


if __name__ == '__main__':
    unittest.main()
