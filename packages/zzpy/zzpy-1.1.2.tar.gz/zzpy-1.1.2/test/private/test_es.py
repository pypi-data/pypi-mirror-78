import zzpy as z
import os
import unittest


class TestCase(unittest.TestCase):
    def test_es_config(self):
        conf = z.EsConfig(
            "es://172.16.2.141:9200|172.16.2.142:9200|172.16.2.143:9200|172.16.2.141:9300|172.16.2.142:9300|172.16.2.143:9300/?user=sca_admin&password=Sdiwi12DI12d")
        self.assertDictEqual(
            conf.params, {"user": "sca_admin", "password": "Sdiwi12DI12d"})
        self.assertListEqual(conf.hosts, ["172.16.2.141:9200",
                                          "172.16.2.142:9200",
                                          "172.16.2.143:9200",
                                          "172.16.2.141:9300",
                                          "172.16.2.142:9300",
                                          "172.16.2.143:9300", ])
