import unittest
from zzpy import randhex
import re


class ZRandomRandhexTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_randhex_when_no_parameters(self):
        for _ in range(10):
            n = randhex()
            self.assertIsInstance(n, str)
            self.assertEqual(len(n), 1)
            self.assertIsNotNone(re.match("^[\dA-F]$", n))

    def test_randhex_when_digits_set(self):
        for digits in range(1, 100):
            n = randhex(digits=digits)
            self.assertIsInstance(n, str)
            self.assertEqual(len(n), digits)
            self.assertIsNotNone(re.match(f"^[\dA-F]{{{digits}}}$", n))

    def test_randhex_when_digits_set_0(self):
        n = randhex(digits=0)
        self.assertIsInstance(n, str)
        self.assertEqual(n, "")

    def test_randhex_when_prefix_set_true(self):
        for digits in range(1, 10):
            n = randhex(digits=digits, prefix=True)
            self.assertIsInstance(n, str)
            self.assertEqual(len(n), 2+digits)
            self.assertIsNotNone(re.match(f"^0x[\dA-F]{{{digits}}}$", n))

    def test_randhex_when_prefix_set_false(self):
        for digits in range(1, 10):
            n = randhex(digits=digits, prefix=False)
            self.assertIsInstance(n, str)
            self.assertEqual(len(n), digits)
            self.assertIsNotNone(re.match(f"^[\dA-F]{{{digits}}}$", n))

    def test_randhex_when_lower_set_true(self):
        digits = 1_000
        self.assertIsNotNone(
            re.match(f"^[\da-f]{{{digits}}}$", randhex(digits=digits, lower=True)))
        self.assertIsNotNone(
            re.match(f"^[\da-f]{{{digits}}}$", randhex(digits=digits, prefix=False, lower=True)))
        self.assertIsNotNone(re.match(
            f"^0x[\da-f]{{{digits}}}$", randhex(digits=digits, prefix=True, lower=True)))

    def test_randhex_when_lower_set_false(self):
        digits = 1_000
        self.assertIsNotNone(
            re.match(f"^[\dA-F]{{{digits}}}$", randhex(digits=digits)))
        self.assertIsNotNone(
            re.match(f"^[\dA-F]{{{digits}}}$", randhex(digits=digits, lower=False)))
        self.assertIsNotNone(
            re.match(f"^[\dA-F]{{{digits}}}$", randhex(digits=digits, prefix=False, lower=False)))
        self.assertIsNotNone(re.match(
            f"^0x[\dA-F]{{{digits}}}$", randhex(digits=digits, prefix=True, lower=False)))
