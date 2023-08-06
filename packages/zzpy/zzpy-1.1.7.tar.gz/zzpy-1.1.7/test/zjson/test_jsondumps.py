import unittest
import datetime
import zzpy as z


class ZjsonJsondumpsTests(unittest.TestCase):
    def test_jsondumps_when_empty_dictionary(self):
        self.assertEqual(z.jsondumps({}), "{}")

    def test_jsondumps_when_empty_string(self):
        self.assertEqual(z.jsondumps(""), "\"\"")

    def test_jsondumps_when_empty_list(self):
        self.assertEqual(z.jsondumps([]), "[]")

    def test_jsondumps_when_contains_datetime(self):
        test_datetime_str = "2020-07-20 12:00:00"
        test_datetime_fmt = "%Y-%m-%d %H:%M:%S"
        d = datetime.datetime.strptime(
            test_datetime_str, test_datetime_fmt)
        expected_value = f'{{"a": 1, "d": "{test_datetime_str}"}}'
        self.assertEqual(z.jsondumps({"a": 1, "d": d}),
                         expected_value)

    def test_jsondumps_when_without_datetime(self):
        expected_value = f'{{"a": 1, "b": "2"}}'
        self.assertEqual(z.jsondumps({"a": 1, "b": "2"}),
                         expected_value)

    def test_jsondumps_with_indent(self):
        expected_value = '{\n    "k": "v"\n}'
        self.assertEqual(z.jsondumps({"k": "v"}, indent=4), expected_value)
