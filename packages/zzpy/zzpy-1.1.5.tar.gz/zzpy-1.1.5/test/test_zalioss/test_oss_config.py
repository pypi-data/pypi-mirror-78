import unittest


class TestCase(unittest.TestCase):
    def test_oss_config(self):
        from zzpy import OssConfig
        url = "oss://zeros.top/b-bucket?key=kkey&secret=ssecret"
        config = OssConfig(url)
        self.assertEqual(config.endpoint, f"https://zeros.top")
        self.assertEqual(config.bucket, "b-bucket")
        self.assertEqual(config.access_key_id, "kkey")
        self.assertEqual(config.access_key_secret, "ssecret")
