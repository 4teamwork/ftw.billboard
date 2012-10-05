from unittest import TestCase
from ftw.billboard.helpers import format_currency


class TestNumberFormatting(TestCase):

   def test_big_number(self):
       self.assertEqual(
           format_currency(12345678.912, decimal_mark='.', thousands_separator=','),
           '12,345,678.91')

   def test_string(self):
       self.assertEqual(
           format_currency('12345678.91', decimal_mark='.', thousands_separator=','),
           '12,345,678.91')

   def test_default(self):
       self.assertEqual(
           format_currency(1234.56),
           '1234.56')

   def test_small_number(self):
       self.assertEqual(
           format_currency(234.56, decimal_mark='.', thousands_separator=','),
           '234.56')

   def test_integer(self):
       self.assertEqual(
           format_currency('12345678', decimal_mark='.', thousands_separator=','),
           '12,345,678')

       self.assertEqual(
           format_currency(12345678, decimal_mark='.', thousands_separator=','),
           '12,345,678')

   def test_only_float(self):
       self.assertEqual(
           format_currency('.123', decimal_mark='.', thousands_separator=','),
           '0.12')
