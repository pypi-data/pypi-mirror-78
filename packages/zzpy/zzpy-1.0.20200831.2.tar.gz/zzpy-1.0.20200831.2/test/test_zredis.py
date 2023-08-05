import unittest


class ZRedisTests(unittest.TestCase):
    def setUp(self):
        import os
        super().setUp()
        self.root_dir = os.path.join("test", "file")
        from zzpy import remove_dir
        remove_dir(self.root_dir)

    def tearDown(self):
        from zzpy import remove_dir
        super().tearDown()
        remove_dir(self.root_dir)

    def test_redis_decode(self):
        from zzpy import redis_decode

        self.assertEqual(redis_decode(b"abc"), u"abc")
        self.assertEqual(redis_decode("你好".encode("utf8")), u"你好")
        self.assertEqual(redis_decode([b"1", "2", 3, u"x".encode("gbk"), u"再见".encode("utf8")]), [
                         u"1", u"2", 3, u"x", u"再见"])
        self.assertEqual(redis_decode(
            (b"1", "2", 3, u"再见".encode("utf8"))), (u"1", u"2", 3, u"再见"))
        self.assertEqual(redis_decode(
            {b"1", "2", 3, u"再见".encode("utf8")}), {u"1", u"2", 3, u"再见"})
