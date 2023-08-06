import unittest
import zzpy as z


def get_now():
    import time
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def get_today():
    return get_date(days=0, separator='-')


def get_date(days=0, separator='-'):
    import time
    return time.strftime(f"%Y{separator}%m{separator}%d", time.localtime(time.time()+days*86400))


class TestCase(unittest.TestCase):
    def test_get_date_with_no_parameters(self):
        self.assertEqual(z.get_date(), get_today())

    def test_get_date_with_days(self):
        for offset in range(-1000, 1000):
            self.assertEqual(z.get_date(offset), get_date(offset))
            self.assertEqual(z.get_date(days=offset), get_date(days=offset))
            self.assertEqual(z.get_date(offset), get_date(offset))
            self.assertEqual(z.get_date(days=offset), get_date(days=offset))

    def test_get_date_with_separator(self):
        self.assertEqual(z.get_date(), get_date(separator="-"))
        self.assertEqual(z.get_date(), z.get_date(separator="-"))
        self.assertEqual(z.get_date(separator="-"), get_date(separator="-"))
        self.assertEqual(z.get_date(separator="/"), get_date(separator="/"))

    def test_get_date_with_days_and_separator(self):
        self.assertEqual(z.get_date(), get_date(days=0, separator="-"))
        self.assertEqual(z.get_date(), z.get_date(days=0, separator="-"))
        self.assertEqual(z.get_date(days=1, separator="*"),
                         get_date(days=1, separator="*"))
        self.assertEqual(z.get_date(days=1, separator="*"),
                         z.get_date(days=1, separator="*"))
        self.assertEqual(z.get_date(days=-1, separator="*"),
                         get_date(days=-1, separator="*"))
        self.assertEqual(z.get_date(days=-1, separator="*"),
                         z.get_date(days=-1, separator="*"))
