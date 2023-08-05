import unittest


class ZMySQLTests(unittest.TestCase):
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

    def test_MySQLConfig(self):
        from zzpy import MySQLConfig

        self.assertEqual(MySQLConfig(url="mysql://1.2.3.4"),
                         MySQLConfig(host="1.2.3.4", port=3306))
        self.assertEqual(MySQLConfig(url="mysql://1.2.3.4/"),
                         MySQLConfig(host="1.2.3.4", port=3306))
        self.assertEqual(MySQLConfig(url="mysql://1.2.3.4:5"),
                         MySQLConfig(host="1.2.3.4", port=5))
        self.assertEqual(MySQLConfig(url="mysql://1.2.3.4:5/d"),
                         MySQLConfig(host="1.2.3.4", port=5, database="d"))
        self.assertEqual(MySQLConfig(url="mysql://1.2.3.4/d"),
                         MySQLConfig(host="1.2.3.4", port=3306, database="d"))
        self.assertEqual(MySQLConfig(url="mysql://1.2.3.4/d?"),
                         MySQLConfig(host="1.2.3.4", port=3306, database="d"))
        self.assertEqual(MySQLConfig(url="mysql://1.2.3.4:5/d?x=1"),
                         MySQLConfig(host="1.2.3.4", port=5, database="d", param={"x": "1"}))
        self.assertEqual(MySQLConfig(url="mysql://1.2.3.4:5/d?x=1&y=2"),
                         MySQLConfig(host="1.2.3.4", port=5, database="d", param={"x": "1", "y": "2"}))

        self.assertEqual(MySQLConfig(url="mysql://localhost"),
                         MySQLConfig(host="localhost", port=3306))
        self.assertEqual(MySQLConfig(url="mysql://localhost/"),
                         MySQLConfig(host="localhost", port=3306))
        self.assertEqual(MySQLConfig(url="mysql://localhost:5"),
                         MySQLConfig(host="localhost", port=5))
        self.assertEqual(MySQLConfig(url="mysql://localhost:5/d"),
                         MySQLConfig(host="localhost", port=5, database="d"))
        self.assertEqual(MySQLConfig(url="mysql://localhost/d"),
                         MySQLConfig(host="localhost", port=3306, database="d"))
        self.assertEqual(MySQLConfig(url="mysql://localhost/d?"),
                         MySQLConfig(host="localhost", port=3306, database="d"))
        self.assertEqual(MySQLConfig(url="mysql://localhost:5/d?x=1"),
                         MySQLConfig(host="localhost", port=5, database="d", param={"x": "1"}))
        self.assertEqual(MySQLConfig(url="mysql://localhost:5/d?x=1&y=2"),
                         MySQLConfig(host="localhost", port=5, database="d", param={"x": "1", "y": "2"}))

        self.assertEqual(MySQLConfig(url="mysql://a"),
                         MySQLConfig(host="a", port=3306))
        self.assertEqual(MySQLConfig(url="mysql://a/"),
                         MySQLConfig(host="a", port=3306))
        self.assertEqual(MySQLConfig(url="mysql://a:5"),
                         MySQLConfig(host="a", port=5))
        self.assertEqual(MySQLConfig(url="mysql://a:5/d"),
                         MySQLConfig(host="a", port=5, database="d"))
        self.assertEqual(MySQLConfig(url="mysql://a/d"),
                         MySQLConfig(host="a", port=3306, database="d"))
        self.assertEqual(MySQLConfig(url="mysql://a/d?"),
                         MySQLConfig(host="a", port=3306, database="d"))
        self.assertEqual(MySQLConfig(url="mysql://a:5/d?x=1"),
                         MySQLConfig(host="a", port=5, database="d", param={"x": "1"}))
        self.assertEqual(MySQLConfig(url="mysql://a:5/d?x=1&y=2"),
                         MySQLConfig(host="a", port=5, database="d", param={"x": "1", "y": "2"}))

        self.assertEqual(MySQLConfig(url="1.2.3.4"),
                         MySQLConfig(host="1.2.3.4", port=3306))
        self.assertEqual(MySQLConfig(url="1.2.3.4/"),
                         MySQLConfig(host="1.2.3.4", port=3306))
        self.assertEqual(MySQLConfig(url="1.2.3.4:5"),
                         MySQLConfig(host="1.2.3.4", port=5))
        self.assertEqual(MySQLConfig(url="1.2.3.4:5/d"),
                         MySQLConfig(host="1.2.3.4", port=5, database="d"))
        self.assertEqual(MySQLConfig(url="1.2.3.4/d"),
                         MySQLConfig(host="1.2.3.4", port=3306, database="d"))
        self.assertEqual(MySQLConfig(url="1.2.3.4/d?"),
                         MySQLConfig(host="1.2.3.4", port=3306, database="d"))
        self.assertEqual(MySQLConfig(url="1.2.3.4:5/d?x=1"),
                         MySQLConfig(host="1.2.3.4", port=5, database="d", param={"x": "1"}))
        self.assertEqual(MySQLConfig(url="1.2.3.4:5/d?x=1&y=2"),
                         MySQLConfig(host="1.2.3.4", port=5, database="d", param={"x": "1", "y": "2"}))

        self.assertEqual(MySQLConfig(url="localhost"),
                         MySQLConfig(host="localhost", port=3306))
        self.assertEqual(MySQLConfig(url="localhost/"),
                         MySQLConfig(host="localhost", port=3306))
        self.assertEqual(MySQLConfig(url="localhost:5"),
                         MySQLConfig(host="localhost", port=5))
        self.assertEqual(MySQLConfig(url="localhost:5/d"),
                         MySQLConfig(host="localhost", port=5, database="d"))
        self.assertEqual(MySQLConfig(url="localhost/d"),
                         MySQLConfig(host="localhost", port=3306, database="d"))
        self.assertEqual(MySQLConfig(url="localhost/d?"),
                         MySQLConfig(host="localhost", port=3306, database="d"))
        self.assertEqual(MySQLConfig(url="localhost:5/d?x=1"),
                         MySQLConfig(host="localhost", port=5, database="d", param={"x": "1"}))
        self.assertEqual(MySQLConfig(url="localhost:5/d?x=1&y=2"),
                         MySQLConfig(host="localhost", port=5, database="d", param={"x": "1", "y": "2"}))

        self.assertEqual(MySQLConfig(url="a"),
                         MySQLConfig(host="a", port=3306))
        self.assertEqual(MySQLConfig(url="a/"),
                         MySQLConfig(host="a", port=3306))
        self.assertEqual(MySQLConfig(url="a:5"),
                         MySQLConfig(host="a", port=5))
        self.assertEqual(MySQLConfig(url="a:5/d"),
                         MySQLConfig(host="a", port=5, database="d"))
        self.assertEqual(MySQLConfig(url="a/d"),
                         MySQLConfig(host="a", port=3306, database="d"))
        self.assertEqual(MySQLConfig(url="a/d?"),
                         MySQLConfig(host="a", port=3306, database="d"))
        self.assertEqual(MySQLConfig(url="a:5/d?x=1"),
                         MySQLConfig(host="a", port=5, database="d", param={"x": "1"}))
        self.assertEqual(MySQLConfig(url="a:5/d?x=1&y=2"),
                         MySQLConfig(host="a", port=5, database="d", param={"x": "1", "y": "2"}))

        self.assertEqual(MySQLConfig(url="mysql://a.b.c:123/?user=uuuu&password=pppp").to_dict(), {
                         "host": "a.b.c", "port": 123, "user": "uuuu", "password": "pppp", "param": {"user": "uuuu", "password": "pppp"}, "url": "mysql://a.b.c:123/?user=uuuu&password=pppp"})
