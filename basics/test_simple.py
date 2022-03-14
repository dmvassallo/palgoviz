#!/usr/bin/env python

"""Tests for the simple code in simple.py."""

import unittest

from simple import MY_NONE, Widget


class TestMyNone(unittest.TestCase):
    """The MY_NONE constant doesn't need any tests. Here's one anyway."""

    __slots__ = ()

    def test_my_none_is_none(self):
        self.assertIsNone(MY_NONE)


# TODO: Extract common code to a setUp method.
class TestWidget(unittest.TestCase):
    """Tests for the Widget class."""

    __slots__ = ()

    def test_size_attribute_has_size(self):
        widget = Widget('vast', 'mauve')
        self.assertEqual(widget.size, 'vast')

    def test_color_attribute_has_color(self):
        widget = Widget('vast', 'mauve')
        self.assertEqual(widget.color, 'mauve')

    def test_size_can_be_changed(self):
        widget = Widget('vast', 'mauve')
        widget.size = 'just barely visible'
        self.assertEqual(widget.size, 'just barely visible')

    def test_color_can_be_changed(self):
        widget = Widget('vast', 'mauve')
        widget.color = 'royal purple'
        self.assertEqual(widget.color, 'royal purple')

    def test_new_attributes_cannot_be_added(self):
        widget = Widget('vast', 'mauve')
        with self.assertRaises(AttributeError):
            widget.favorite_desert = 'Sahara'


if __name__ == '__main__':
    unittest.main()