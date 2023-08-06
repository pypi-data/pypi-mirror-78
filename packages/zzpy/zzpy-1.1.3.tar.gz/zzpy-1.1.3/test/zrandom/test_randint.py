import unittest
from zzpy import randint


class ZRandomRandintTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_randint_when_no_parameters(self):
        for _ in range(10_000):
            n = randint()
            self.assertTrue(0 <= n <= 9)

    def test_randint_when_only_given_min(self):
        for _ in range(10_000):
            n = randint(min=5)
            self.assertTrue(5 <= n <= 9)

    def test_randint_when_only_given_max(self):
        for _ in range(10_000):
            n = randint(max=5)
            self.assertTrue(0 <= n <= 5)

    def test_randint_when_given_min_and_max(self):
        for _ in range(10_000):
            n = randint(min=1, max=5)
            self.assertTrue(1 <= n <= 5)

    def test_randint_when_min_equals_max(self):
        for _ in range(10_000):
            n = randint(min=1, max=1)
            self.assertEqual(n, 1)

    def test_randint_when_min_is_larger_then_max(self):
        for _ in range(10_000):
            n = randint(min=5, max=1)
            self.assertTrue(1 <= n <= 5)
