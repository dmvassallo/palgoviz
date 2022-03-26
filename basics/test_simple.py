#!/usr/bin/env python

"""Tests for the simple code in simple.py."""

from fractions import Fraction
import io
from numbers import Number
import sys
import unittest

from parameterized import parameterized, parameterized_class

from simple import (
    BearBowl,
    MY_NONE,
    MulSquarer,
    PowSquarer,
    Squarer,
    Widget,
    alert,
    answer,
    bail_if,
    is_sorted,
    make_squarer,
)


class TestMyNone(unittest.TestCase):
    """The MY_NONE constant doesn't need any tests. Here's one anyway."""

    def test_my_none_is_none(self):
        self.assertIsNone(MY_NONE)


class TestWidget(unittest.TestCase):
    """Tests for the Widget class."""

    def setUp(self):
        """Make a Widget for testing."""
        self.widget = Widget('vast', 'mauve')  # Arrange

    def test_size_attribute_has_size(self):
        self.assertEqual(self.widget.size, 'vast')

    def test_color_attribute_has_color(self):
        self.assertEqual(self.widget.color, 'mauve')

    def test_size_can_be_changed(self):
        self.widget.size = 'just barely visible'
        self.assertEqual(self.widget.size, 'just barely visible')

    def test_color_can_be_changed(self):
        self.widget.color = 'royal purple'  # Act.
        self.assertEqual(self.widget.color, 'royal purple')  # Assert.

    def test_new_attributes_cannot_be_added(self):
        with self.assertRaises(AttributeError):
            self.widget.favorite_desert = 'Sahara'


class TestAnswer(unittest.TestCase):
    """Test the answer() function."""

    def test_the_answer_is_42(self):
        answer_to_the_question = answer()
        self.assertEqual(answer_to_the_question, 42)

    def test_the_answer_is_an_int(self):
        answer_to_the_question = answer()
        self.assertIsInstance(answer_to_the_question, int)


class TestIsSorted(unittest.TestCase):
    """Tests for the is_sorted function."""

    def test_empty_list_is_sorted(self):
        items = []
        self.assertTrue(is_sorted(items))

    def test_empty_generator_is_sorted(self):
        items = (x for x in ())
        self.assertTrue(is_sorted(items))

    def test_one_element_list_is_sorted(self):
        items = [76]
        self.assertTrue(is_sorted(items))

    def test_one_element_generator_is_sorted(self):
        items = (x for x in (76,))
        self.assertTrue(is_sorted(items))

    def test_ascending_two_element_list_is_sorted(self):
        items = ['a', 'b']
        self.assertTrue(is_sorted(items))

    def test_descending_two_element_list_is_not_sorted(self):
        with self.subTest(kind='strings'):
            items = ['b', 'a']
            self.assertFalse(is_sorted(items))

        with self.subTest(kind='integers'):
            items = [3, 2]
            self.assertFalse(is_sorted(items))

    def test_descending_two_element_generator_is_not_sorted(self):
        with self.subTest(kind='strings'):
            items = (x for x in ('b', 'a'))
            self.assertFalse(is_sorted(items))

        with self.subTest(kind='integers'):
            items = (x for x in (3, 2))
            self.assertFalse(is_sorted(items))

    def test_ascending_two_element_generator_is_sorted(self):
        items = (ch for ch in 'ab')
        self.assertTrue(is_sorted(items))

    def test_equal_two_element_list_is_sorted(self):
        items = ['a', 'a']
        self.assertTrue(is_sorted(items))

    def test_equal_two_element_generator_is_sorted(self):
        items = (ch for ch in 'aa')
        self.assertTrue(is_sorted(items))

    def test_sorted_short_but_nontrivial_list_is_sorted(self):
        items = ['bar', 'baz', 'eggs', 'foo', 'foobar', 'ham', 'quux', 'spam']
        self.assertTrue(is_sorted(items))

    def test_unsorted_short_but_nontrivial_is_unsorted(self):
        items = ['bar', 'eggs', 'foo', 'ham', 'foobar', 'quux', 'baz', 'spam']
        self.assertFalse(is_sorted(items))


class TestAlert(unittest.TestCase):
    """Tests for the alert function."""

    def setUp(self):
        """Redirect standard error."""
        self._old_err = sys.stderr
        self._my_stderr = sys.stderr = io.StringIO()

    def tearDown(self):
        """Restore original standard error."""
        sys.stderr = self._old_err

    @parameterized.expand([
        ("Wall is still up.", "alert: Wall is still up.\n"),
        ("in your base.", "alert: in your base.\n"),
        ("killing your dudes.", "alert: killing your dudes.\n"),
        ('refusing to say hello', 'alert: refusing to say hello\n'),
        ('3609 squirrels complained', 'alert: 3609 squirrels complained\n'),
        ('boycott whalebone skis', 'alert: boycott whalebone skis\n'),
    ])
    def test_alert_and_newline_are_printed_with_string(self, message, expected):
        alert(message)
        self.assertEqual(self._actual, expected)

    def test_alert_with_nonstring_message_prints_str_of_message(self):
        message = Fraction(2, 3)
        expected = "alert: 2/3\n"
        alert(message)
        self.assertEqual(self._actual, expected)

    @property
    def _actual(self):
        """Result printed by alert()."""
        return self._my_stderr.getvalue()


class TestBailIf(unittest.TestCase):
    """Tests for the bail_if function."""

    def test_bails_if_truthy(self):
        for value in (True, 1, 1.1, 'hello', object()):
            with self.subTest(value=value):
                with self.assertRaises(SystemExit) as cm:
                    bail_if(value)
                self.assertEqual(cm.exception.code, 1)

    def test_does_not_bail_if_falsey(self):
        for value in (False, 0, 0.0, '', None):
            with self.subTest(value=value):
                try:
                    bail_if(value)
                except SystemExit:
                    self.fail("Bailed although condition was falsey.")


@parameterized_class(('name', 'implementation'), [
    ('Mul', MulSquarer),
    ('Pow', PowSquarer),
    ('func', staticmethod(make_squarer)),
])
class TestAllSquarers(unittest.TestCase):
    """Tests for any kind of Squarer."""

    @parameterized.expand([
        ('pos_0', 0, 0),
        ('pos_1', 1, 1),
        ('pos_2', 2, 4),
        ('pos_3', 3, 9),
    ])
    def test_positive_ints_are_squared(self, _name, num, expected):
        squarer = self.implementation()
        self.assertEqual(squarer(num), expected)

    @parameterized.expand([
        ('pos_0.0', 0.0, 0.0),
        ('pos_1.0', 1.0, 1.0),
        ('pos_2.2', 2.2, 4.84),
        ('pos_3.1', 3.1, 9.61),
    ])
    def test_positive_floats_are_squared(self, _name, num, expected):
        squarer = self.implementation()
        self.assertAlmostEqual(squarer(num), expected)

    @parameterized.expand([
        ('neg_1', -1, 1),
        ('neg_2', -2, 4),
        ('neg_3', -3, 9),
        ('neg_4', -4, 16),
    ])
    def test_negative_ints_are_squared(self, _name, num, expected):
        squarer = self.implementation()
        self.assertEqual(squarer(num), expected)

    @parameterized.expand([
        ('neg_1.2', -1.2, 1.44),
        ('neg_1.0', -1.0, 1.0),
        ('neg_2.2', -2.2, 4.84),
        ('neg_3.1', -3.1, 9.61),
    ])
    def test_negative_floats_are_squared(self, _name, num, expected):
        squarer = self.implementation()
        self.assertAlmostEqual(squarer(num), expected)


class TestSquarerClasses(unittest.TestCase):
    """Tests for the custom Squarer classes."""

    _SQUARERS = [
        ('Mul', MulSquarer),
        ('Pow', PowSquarer),
    ]

    @parameterized.expand([
        ('Mul', MulSquarer, 'MulSquarer()'),
        ('Pow', PowSquarer, 'PowSquarer()'),
    ])
    def test_repr(self, _name, impl, expected):
        """repr shows type and looks like Python code."""
        squarer = impl()
        self.assertEqual(repr(squarer), expected)

    @parameterized.expand(_SQUARERS)
    def test_squarer_is_a_squarer(self, _name, impl):
        squarer = impl()
        self.assertIsInstance(squarer, Squarer)

    @parameterized.expand(_SQUARERS)
    def test_squarers_of_same_type_are_equal(self, _name, impl):
        squarer1 = impl()
        squarer2 = impl()
        self.assertEqual(squarer1, squarer2)

    @parameterized.expand([
        ('Mul, Pow', MulSquarer, PowSquarer),
        ('Pow, Mul', PowSquarer, MulSquarer),
    ])
    def test_squarers_of_different_types_are_not_equal(self, _name,
                                                       impl1, impl2):
        squarer1 = impl1()
        squarer2 = impl2()
        self.assertNotEqual(squarer1, squarer2)

    @parameterized.expand(_SQUARERS)
    def test_squarers_of_same_type_hash_equal(self, _name, impl):
        squarer1 = impl()
        squarer2 = impl()
        self.assertEqual(hash(squarer1), hash(squarer2))


class TestBearBowl(unittest.TestCase):
    """
    Tests for the BearBowl class.

    TODO: I have separated most test methods below into groups, each described
    by a comment. This suggests that the groups should be written as individual
    methods, with parameterization. Decide whether to do this and, if so, how.
    """

    # The three bowls really are bowls:

    def test_too_cold_is_a_bowl(self):
        self.assertIsInstance(BearBowl.TOO_COLD, BearBowl)

    def test_just_right_is_a_bowl(self):
        self.assertIsInstance(BearBowl.JUST_RIGHT, BearBowl)

    def test_too_hot_is_a_bowl(self):
        self.assertIsInstance(BearBowl.TOO_HOT, BearBowl)

    # They are not numbers:

    def test_too_cold_is_not_a_number(self):
        self.assertNotIsInstance(BearBowl.TOO_COLD, Number)

    def test_just_right_is_not_a_number(self):
        self.assertNotIsInstance(BearBowl.JUST_RIGHT, Number)

    def test_too_hot_is_not_a_number(self):
        self.assertNotIsInstance(BearBowl.TOO_HOT, Number)

    # Their reprs are code that evaluates to them (if BearBowl is in scope):

    def test_too_cold_repr_shows_attribute_access_from_class(self):
        self.assertEqual(repr(BearBowl.TOO_COLD), 'BearBowl.TOO_COLD')

    def test_just_right_repr_shows_attribute_access_from_class(self):
        self.assertEqual(repr(BearBowl.JUST_RIGHT), 'BearBowl.JUST_RIGHT')

    def test_too_hot_repr_shows_attribute_access_from_class(self):
        self.assertEqual(repr(BearBowl.TOO_HOT), 'BearBowl.TOO_HOT')

    # Their strs are that same code that evaluates to them:

    def test_too_cold_str_shows_attribute_access_from_class(self):
        self.assertEqual(str(BearBowl.TOO_COLD), 'BearBowl.TOO_COLD')

    def test_just_right_str_shows_attribute_access_from_class(self):
        self.assertEqual(str(BearBowl.JUST_RIGHT), 'BearBowl.JUST_RIGHT')

    def test_too_hot_str_shows_attribute_access_from_class(self):
        self.assertEqual(str(BearBowl.TOO_HOT), 'BearBowl.TOO_HOT')

    # They know their names, accessible through the name attribute:

    def test_too_cold_name_attribute_is_too_cold(self):
        self.assertEqual(BearBowl.TOO_COLD.name, 'TOO_COLD')

    def test_just_right_name_attribute_is_just_right(self):
        self.assertEqual(BearBowl.JUST_RIGHT.name, 'JUST_RIGHT')

    def test_too_hot_name_attribute_is_too_hot(self):
        self.assertEqual(BearBowl.TOO_HOT.name, 'TOO_HOT')

    # They are, as one would expect, equal to themselves:

    def test_too_cold_equals_too_cold(self):
        self.assertEqual(BearBowl.TOO_COLD, BearBowl.TOO_COLD)

    def test_just_right_equals_just_right(self):
        self.assertEqual(BearBowl.JUST_RIGHT, BearBowl.JUST_RIGHT)

    def test_too_hot_equals_too_hot(self):
        self.assertEqual(BearBowl.TOO_HOT, BearBowl.TOO_HOT)

    # They (i.e., differently named bowls) are not equal to each other:

    def test_too_cold_not_equal_to_just_right(self):
        with self.subTest(lhs=BearBowl.TOO_COLD, rhs=BearBowl.JUST_RIGHT):
            self.assertNotEqual(BearBowl.TOO_COLD, BearBowl.JUST_RIGHT)
        with self.subTest(lhs=BearBowl.JUST_RIGHT, rhs=BearBowl.TOO_COLD):
            self.assertNotEqual(BearBowl.JUST_RIGHT, BearBowl.TOO_COLD)

    def test_too_cold_not_equal_to_too_hot(self):
        with self.subTest(lhs=BearBowl.TOO_COLD, rhs=BearBowl.TOO_HOT):
            self.assertNotEqual(BearBowl.TOO_COLD, BearBowl.TOO_HOT)
        with self.subTest(lhs=BearBowl.TOO_HOT, rhs=BearBowl.TOO_COLD):
            self.assertNotEqual(BearBowl.TOO_HOT, BearBowl.TOO_COLD)

    def test_just_right_not_equal_to_too_hot(self):
        with self.subTest(lhs=BearBowl.JUST_RIGHT, rhs=BearBowl.TOO_HOT):
            self.assertNotEqual(BearBowl.JUST_RIGHT, BearBowl.TOO_HOT)
        with self.subTest(lhs=BearBowl.TOO_HOT, rhs=BearBowl.JUST_RIGHT):
            self.assertNotEqual(BearBowl.TOO_HOT, BearBowl.JUST_RIGHT)

    # Cooler bowls compare less than warmer bowls:

    def test_too_cold_less_than_just_right(self):
        self.assertLess(BearBowl.TOO_COLD, BearBowl.JUST_RIGHT)

    def test_too_cold_less_than_too_hot(self):
        self.assertLess(BearBowl.TOO_COLD, BearBowl.TOO_HOT)

    def test_just_right_less_than_too_hot(self):
        self.assertLess(BearBowl.JUST_RIGHT, BearBowl.TOO_HOT)

    # Warmer bowls compare greater than cooler bowls:

    def test_just_right_greater_than_too_cold(self):
        self.assertGreater(BearBowl.JUST_RIGHT, BearBowl.TOO_COLD)

    def test_too_hot_greater_than_too_cold(self):
        self.assertGreater(BearBowl.TOO_HOT, BearBowl.TOO_COLD)

    def test_too_hot_greater_than_just_right(self):
        self.assertGreater(BearBowl.TOO_HOT, BearBowl.JUST_RIGHT)

    # Bowls compare less than or equal to bowls that are no warmer:

    def test_too_cold_less_than_or_equal_to_itself(self):
        self.assertLessEqual(BearBowl.TOO_COLD, BearBowl.TOO_COLD)

    def test_too_cold_less_than_or_equal_to_just_right(self):
        self.assertLessEqual(BearBowl.TOO_COLD, BearBowl.JUST_RIGHT)

    def test_too_cold_less_than_or_equal_to_too_hot(self):
        self.assertLessEqual(BearBowl.TOO_COLD, BearBowl.TOO_HOT)

    def test_just_right_less_than_or_equal_to_itself(self):
        self.assertLessEqual(BearBowl.JUST_RIGHT, BearBowl.JUST_RIGHT)

    def test_just_right_less_than_or_equal_to_too_hot(self):
        self.assertLessEqual(BearBowl.JUST_RIGHT, BearBowl.TOO_HOT)

    def test_too_hot_less_than_or_equal_to_itself(self):
        self.assertLessEqual(BearBowl.TOO_HOT, BearBowl.TOO_HOT)

    # Bowls compare greater than or equal to bowls that are no cooler:

    def test_too_cold_greater_than_or_equal_to_itself(self):
        self.assertGreaterEqual(BearBowl.TOO_COLD, BearBowl.TOO_COLD)

    def test_just_right_greater_than_or_equal_to_too_cold(self):
        self.assertGreaterEqual(BearBowl.JUST_RIGHT, BearBowl.TOO_COLD)

    def test_just_right_greater_than_or_equal_to_itself(self):
        self.assertGreaterEqual(BearBowl.JUST_RIGHT, BearBowl.JUST_RIGHT)

    def test_too_hot_greater_than_or_equal_to_too_cold(self):
        self.assertGreaterEqual(BearBowl.TOO_HOT, BearBowl.TOO_COLD)

    def test_too_hot_greater_than_or_equal_to_just_right(self):
        self.assertGreaterEqual(BearBowl.TOO_HOT, BearBowl.JUST_RIGHT)

    def test_too_hot_greater_than_or_equal_to_itself(self):
        self.assertGreaterEqual(BearBowl.TOO_HOT, BearBowl.TOO_HOT)


if __name__ == '__main__':
    unittest.main()
