#!/usr/bin/env python

"""Tests for `vodafone_ie_account_checker` package."""
import unittest

from vodafone_ie_account_checker import api


class TestVodafone_ie_account_checker(unittest.TestCase):
    """Tests for `vodafone_ie_account_checker` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_exception_on_account_no_username(self):
        """Test exception when no username passed."""
        self.assertRaises(Exception, lambda: api.Account(password='test'))

    def test_exception_on_account_no_password(self):
        """Test exception when no password passed."""
        self.assertRaises(Exception, lambda: api.Account(username='test'))
