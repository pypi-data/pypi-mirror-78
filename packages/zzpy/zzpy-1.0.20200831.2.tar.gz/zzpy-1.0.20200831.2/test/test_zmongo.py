import unittest


class ZMongoTests(unittest.TestCase):
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

    def test_mongo_config(self):
        from zzpy import MongoConfig

        self.assertEqual(MongoConfig(url="mongodb://1.2.3.4"),
                         MongoConfig(host="1.2.3.4", port=27017))
        
        self.assertEqual(MongoConfig(url="mongodb://1.2.3.4/"),
                         MongoConfig(host="1.2.3.4", port=27017))
        self.assertEqual(MongoConfig(url="mongodb://1.2.3.4:5"),
                         MongoConfig(host="1.2.3.4", port=5))
        self.assertEqual(MongoConfig(url="mongodb://1.2.3.4:5/d"),
                         MongoConfig(host="1.2.3.4", port=5, database="d"))
        self.assertEqual(MongoConfig(url="mongodb://1.2.3.4/d"),
                         MongoConfig(host="1.2.3.4", port=27017, database="d"))
        self.assertEqual(MongoConfig(url="mongodb://1.2.3.4/d?"),
                         MongoConfig(host="1.2.3.4", port=27017, database="d"))
        self.assertEqual(MongoConfig(url="mongodb://1.2.3.4:5/d?x=1"),
                         MongoConfig(host="1.2.3.4", port=5, database="d", param={"x": "1"}))
        self.assertEqual(MongoConfig(url="mongodb://1.2.3.4:5/d?x=1&y=2"),
                         MongoConfig(host="1.2.3.4", port=5, database="d", param={"x": "1", "y": "2"}))

        self.assertEqual(MongoConfig(url="mongodb://localhost"),
                         MongoConfig(host="localhost", port=27017))
        self.assertEqual(MongoConfig(url="mongodb://localhost/"),
                         MongoConfig(host="localhost", port=27017))
        self.assertEqual(MongoConfig(url="mongodb://localhost:5"),
                         MongoConfig(host="localhost", port=5))
        self.assertEqual(MongoConfig(url="mongodb://localhost:5/d"),
                         MongoConfig(host="localhost", port=5, database="d"))
        self.assertEqual(MongoConfig(url="mongodb://localhost/d"),
                         MongoConfig(host="localhost", port=27017, database="d"))
        self.assertEqual(MongoConfig(url="mongodb://localhost/d?"),
                         MongoConfig(host="localhost", port=27017, database="d"))
        self.assertEqual(MongoConfig(url="mongodb://localhost:5/d?x=1"),
                         MongoConfig(host="localhost", port=5, database="d", param={"x": "1"}))
        self.assertEqual(MongoConfig(url="mongodb://localhost:5/d?x=1&y=2"),
                         MongoConfig(host="localhost", port=5, database="d", param={"x": "1", "y": "2"}))

        self.assertEqual(MongoConfig(url="mongodb://a"),
                         MongoConfig(host="a", port=27017))
        self.assertEqual(MongoConfig(url="mongodb://a/"),
                         MongoConfig(host="a", port=27017))
        self.assertEqual(MongoConfig(url="mongodb://a:5"),
                         MongoConfig(host="a", port=5))
        self.assertEqual(MongoConfig(url="mongodb://a:5/d"),
                         MongoConfig(host="a", port=5, database="d"))
        self.assertEqual(MongoConfig(url="mongodb://a/d"),
                         MongoConfig(host="a", port=27017, database="d"))
        self.assertEqual(MongoConfig(url="mongodb://a/d?"),
                         MongoConfig(host="a", port=27017, database="d"))
        self.assertEqual(MongoConfig(url="mongodb://a:5/d?x=1"),
                         MongoConfig(host="a", port=5, database="d", param={"x": "1"}))
        self.assertEqual(MongoConfig(url="mongodb://a:5/d?x=1&y=2"),
                         MongoConfig(host="a", port=5, database="d", param={"x": "1", "y": "2"}))

        self.assertEqual(MongoConfig(url="1.2.3.4"),
                         MongoConfig(host="1.2.3.4", port=27017))
        self.assertEqual(MongoConfig(url="1.2.3.4/"),
                         MongoConfig(host="1.2.3.4", port=27017))
        self.assertEqual(MongoConfig(url="1.2.3.4:5"),
                         MongoConfig(host="1.2.3.4", port=5))
        self.assertEqual(MongoConfig(url="1.2.3.4:5/d"),
                         MongoConfig(host="1.2.3.4", port=5, database="d"))
        self.assertEqual(MongoConfig(url="1.2.3.4/d"),
                         MongoConfig(host="1.2.3.4", port=27017, database="d"))
        self.assertEqual(MongoConfig(url="1.2.3.4/d?"),
                         MongoConfig(host="1.2.3.4", port=27017, database="d"))
        self.assertEqual(MongoConfig(url="1.2.3.4:5/d?x=1"),
                         MongoConfig(host="1.2.3.4", port=5, database="d", param={"x": "1"}))
        self.assertEqual(MongoConfig(url="1.2.3.4:5/d?x=1&y=2"),
                         MongoConfig(host="1.2.3.4", port=5, database="d", param={"x": "1", "y": "2"}))

        self.assertEqual(MongoConfig(url="localhost"),
                         MongoConfig(host="localhost", port=27017))
        self.assertEqual(MongoConfig(url="localhost/"),
                         MongoConfig(host="localhost", port=27017))
        self.assertEqual(MongoConfig(url="localhost:5"),
                         MongoConfig(host="localhost", port=5))
        self.assertEqual(MongoConfig(url="localhost:5/d"),
                         MongoConfig(host="localhost", port=5, database="d"))
        self.assertEqual(MongoConfig(url="localhost/d"),
                         MongoConfig(host="localhost", port=27017, database="d"))
        self.assertEqual(MongoConfig(url="localhost/d?"),
                         MongoConfig(host="localhost", port=27017, database="d"))
        self.assertEqual(MongoConfig(url="localhost:5/d?x=1"),
                         MongoConfig(host="localhost", port=5, database="d", param={"x": "1"}))
        self.assertEqual(MongoConfig(url="localhost:5/d?x=1&y=2"),
                         MongoConfig(host="localhost", port=5, database="d", param={"x": "1", "y": "2"}))

        self.assertEqual(MongoConfig(url="a"),
                         MongoConfig(host="a", port=27017))
        self.assertEqual(MongoConfig(url="a/"),
                         MongoConfig(host="a", port=27017))
        self.assertEqual(MongoConfig(url="a:5"),
                         MongoConfig(host="a", port=5))
        self.assertEqual(MongoConfig(url="a:5/d"),
                         MongoConfig(host="a", port=5, database="d"))
        self.assertEqual(MongoConfig(url="a/d"),
                         MongoConfig(host="a", port=27017, database="d"))
        self.assertEqual(MongoConfig(url="a/d?"),
                         MongoConfig(host="a", port=27017, database="d"))
        self.assertEqual(MongoConfig(url="a:5/d?x=1"),
                         MongoConfig(host="a", port=5, database="d", param={"x": "1"}))
        self.assertEqual(MongoConfig(url="a:5/d?x=1&y=2"),
                         MongoConfig(host="a", port=5, database="d", param={"x": "1", "y": "2"}))
