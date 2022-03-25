#!/usr/bin/env python

"""Tests for the simple code in simple.py."""

from fractions import Fraction
import io
import sys
import unittest

from parameterized import parameterized, parameterized_class

from simple import (
    MY_NONE,
    Squarer,
    make_squarer,
    MulSquarer,
    PowSquarer,
    Widget,
    answer,
    is_sorted,
    alert,
    bail_if)


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

    @parameterized.expand([
        ('Mul', MulSquarer),
        ('Pow', PowSquarer),
    ])
    def test_repr(self, _name, implementation):
        """repr shows type and looks like Python code."""
        expected = f'{implementation.__name__}()'
        squarer = implementation()
        self.assertEqual(repr(squarer), expected)

    @parameterized.expand([
        ('Mul', MulSquarer),
        ('Pow', PowSquarer),
    ])
    def test_squarer_is_a_squarer(self, _name, implementation):
        squarer = implementation()
        self.assertIsInstance(squarer, Squarer)

    @parameterized.expand([
        ('Mul', MulSquarer),
        ('Pow', PowSquarer),
    ])
    def test_two_squarers_of_same_type_are_equal(self, _name, implementation):
        squarer1 = implementation()
        squarer2 = implementation()
        self.assertEqual(squarer1, squarer2)

    def test_a_MulSquarer_is_not_equal_to_a_PowSquarer(self):
        squarer1 = MulSquarer()
        squarer2 = PowSquarer()
        self.assertNotEqual(squarer1, squarer2)

    def test_a_PowSquarer_is_not_equal_to_a_MulSquarer(self):
        squarer1 = PowSquarer()
        squarer2 = MulSquarer()
        self.assertNotEqual(squarer1, squarer2)


if __name__ == '__main__':
    unittest.main()
