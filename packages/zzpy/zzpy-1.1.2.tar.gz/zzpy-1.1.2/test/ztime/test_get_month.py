import unittest
import zzpy as z


def get_month(months=0, separator='-'):
    import arrow
    return arrow.now().shift(months=months).format(f"YYYY{separator}MM")


class TestCase(unittest.TestCase):
    def test_get_month_with_no_parameters(self):
        self.assertEqual(z.get_month(), get_month())

    def test_get_month_with_days(self):
        for offset in range(-1000, 1000):
            self.assertEqual(z.get_month(offset), get_month(offset))
            self.assertEqual(z.get_month(months=offset),
                             get_month(months=offset))
            self.assertEqual(z.get_month(offset), get_month(offset))
            self.assertEqual(z.get_month(months=offset),
                             get_month(months=offset))

    def test_get_month_with_separator(self):
        self.assertEqual(z.get_month(), get_month(separator="-"))
        self.assertEqual(z.get_month(), z.get_month(separator="-"))
        self.assertEqual(z.get_month(separator="-"), get_month(separator="-"))
        self.assertEqual(z.get_month(separator="/"), get_month(separator="/"))

    def test_get_month_with_days_and_separator(self):
        self.assertEqual(z.get_month(), get_month(months=0, separator="-"))
        self.assertEqual(z.get_month(), z.get_month(months=0, separator="-"))
        self.assertEqual(z.get_month(months=1, separator="*"),
                         get_month(months=1, separator="*"))
        self.assertEqual(z.get_month(months=1, separator="*"),
                         z.get_month(months=1, separator="*"))
        self.assertEqual(z.get_month(months=-1, separator="*"),
                         get_month(months=-1, separator="*"))
        self.assertEqual(z.get_month(months=-1, separator="*"),
                         z.get_month(months=-1, separator="*"))
