import unittest


class ZGeoTests(unittest.TestCase):
    def test_amap_geo_coding(self):
        from zzpy import amap_geo_coding
        with self.assertRaises(AssertionError):
            amap_geo_coding(address="大连市腾讯大厦")
        with self.assertRaises(AssertionError):
            amap_geo_coding(address="大连市腾讯大厦", api_key="")
        with self.assertRaises(Exception):
            amap_geo_coding(address="大连市腾讯大厦", api_key="WRONG_API_KEY")
