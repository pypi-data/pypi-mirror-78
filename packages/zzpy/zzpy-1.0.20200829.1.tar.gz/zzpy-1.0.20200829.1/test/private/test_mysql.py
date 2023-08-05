import unittest
import datetime
import zzpy as z


class TestCase(unittest.TestCase):
    def setUp(self):
        self.client = z.mysql_connect(url="mysql://am-8vb369k7zxdt10tz043750.zhangbei.ads.aliyuncs.com:3306/?user=amap_dba&password=sNDfwkdl6SDfw33")
    
    def tearDown(self):
        self.client.close()
        self.client = None
    
    def test_mysql_connect(self):
        client = z.mysql_connect(url="mysql://am-8vb369k7zxdt10tz043750.zhangbei.ads.aliyuncs.com:3306/?user=amap_dba&password=sNDfwkdl6SDfw33")
        self.assertIsNotNone(client)
        client.close()
        
    def test_mysql_count_table(self):
        a = z.mysql_count_table(self.client, table="sca.t_std_org")
        self.assertGreater(a, 0)
        b = z.mysql_count_table(self.client, table="sca.t_std_org", where_condition="is_deleted=0")
        self.assertGreater(b, 0)
        self.assertGreater(a, b)
    
    def test_mysql_iter_table(self):
        res = set()
        for it in z.mysql_iter_table(self.client, table="sca.t_std_org", where_condition="is_deleted=0", offset_limit="limit 10"):
            res.add(it["code"])
        self.assertEqual(len(res), 10)
        
        for it in z.mysql_iter_table(self.client, table="sca.t_std_org", fields={"code"}, where_condition="is_deleted=0", offset_limit="limit 10"):
            self.assertSetEqual(set(it.keys()), {"code"})
        
        for it in z.mysql_iter_table(self.client, table="sca.t_std_org", fields={"code", "name"}, where_condition="is_deleted=0", offset_limit="limit 10"):
            self.assertSetEqual(set(it.keys()), {"code", "name"})