import unittest


class ZconfigTests(unittest.TestCase):
    def setUp(self):
        import os
        super().setUp()
        self.root_dir = os.path.join("test", "file")
        from zzpy import init_dir
        init_dir(self.root_dir)

    def tearDown(self):
        from zzpy import remove_dir
        super().tearDown()
        remove_dir(self.root_dir)

    def test_get_param_none(self):
        from zzpy import get_param
        key = "UNITTEST_KEY"

        value = get_param(key)
        self.assertIsNone(value)

    def test_get_param_from_default_value(self):
        from zzpy import get_param
        key = "UNITTEST_KEY"
        default_value = "UNITTEST_DEFAULT"
        value = get_param(key, default_value=default_value)
        self.assertEqual(value, default_value)

    def test_get_param_from_default_config_value(self):
        from zzpy import get_param
        from zzpy import write_file
        import os
        import json

        key = "UNITTEST_KEY"

        default_config_path = os.path.join(
            self.root_dir, "default-config.json")
        default_config_value = "UNITTEST_DEFAULT_CONF"
        write_file(json.dumps(
            {key: default_config_value}), default_config_path)

        default_value = "UNITTEST_DEFAULT"

        value = get_param(key, default_value=default_value,
                          default_config_path=default_config_path, local_config_path=None)
        self.assertEqual(value, default_config_value)

    def test_get_param_from_local_config_value(self):
        from zzpy import get_param
        from zzpy import write_file
        import os
        import json

        key = "UNITTEST_KEY"

        local_config_path = os.path.join(self.root_dir, "local-config.json")
        local_config_value = "UNITTEST_LOCAL_CONF"
        write_file(json.dumps({key: local_config_value}), local_config_path)

        default_config_path = os.path.join(
            self.root_dir, "default-config.json")
        default_config_value = "UNITTEST_DEFAULT_CONF"
        write_file(json.dumps(
            {key: default_config_value}), default_config_path)

        default_value = "UNITTEST_DEFAULT"

        value = get_param(key, default_value=default_value,
                          default_config_path=default_config_path, local_config_path=local_config_path)
        self.assertEqual(value, local_config_value)

    def test_get_param_from_env(self):
        from zzpy import get_param
        from zzpy import write_file
        import os
        import json

        # init
        key = "UNITTEST_KEY"
        env_value = "UNITTEST_ENV"
        local_config_path = os.path.join(self.root_dir, "local-config.json")
        local_config_value = "UNITTEST_LOCAL_CONF"
        write_file(json.dumps({key: local_config_value}), local_config_path)

        default_config_path = os.path.join(
            self.root_dir, "default-config.json")
        default_config_value = "UNITTEST_DEFAULT_CONF"
        write_file(json.dumps(
            {key: default_config_value}), default_config_path)

        default_value = "UNITTEST_DEFAULT"

        os.environ[key] = env_value
        self.assertIn(key, os.environ)

        value = get_param(key, default_value=default_value,
                          default_config_path=default_config_path, local_config_path=local_config_path)
        self.assertEqual(value, env_value)

        # clean
        del os.environ[key]
        self.assertNotIn(key, os.environ)
