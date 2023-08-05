import unittest


class ZfileTests(unittest.TestCase):
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

    def test_read_jsonline(self):
        from zzpy import read_jsonline
        from collections.abc import Generator
        import os

        # generator
        file_path = os.path.join("test", "static", "1.jsonl")
        self.assertIsInstance(read_jsonline(file_path), Generator)

        # end file without newline
        data = []
        for i in read_jsonline(file_path):
            data.append(i)
        self.assertListEqual(data, [{"name": "Zero", "age": 31},
                                    {"name": "Flyoung", "age": 17}])

        # generator
        file_path = os.path.join("test", "static", "2.jsonl")
        self.assertIsInstance(read_jsonline(file_path), Generator)

        # end file with newline
        data = []
        for i in read_jsonline(file_path):
            data.append(i)
        self.assertListEqual(data, [{"name": "Zero", "age": 31},
                                    {"name": "Flyoung", "age": 17}])

    def test_create_and_remove_dir(self):
        """测试文件夹的创建和删除"""
        from zzpy import create_dir, remove_dir, init_dir
        from zzpy import get_file_name_list_from_dir
        import os

        # ending without "/"
        a_dir = os.path.join(self.root_dir, "a")
        b_dir = os.path.join(self.root_dir, "a", "b")

        create_dir(b_dir)
        self.assertTrue(os.path.exists(b_dir))

        init_dir(a_dir)
        self.assertTrue(os.path.exists(a_dir))
        self.assertFalse(os.path.exists(b_dir))

    def test_create_and_remove_dir_ending_with_slash(self):
        """测试文件夹名最后带斜线/的创建和删除"""
        from zzpy import create_dir, remove_dir, init_dir
        import os

        # ending with "/"
        a_dir = os.path.join(self.root_dir, "a/")
        b_dir = os.path.join(self.root_dir, "a", "b/")

        create_dir(b_dir)
        self.assertTrue(os.path.exists(b_dir))

        init_dir(a_dir)
        self.assertTrue(os.path.exists(a_dir))
        self.assertFalse(os.path.exists(b_dir))

    def test_init_dirs(self):
        from zzpy import init_dirs
        from zzpy import get_tmp_dir_path
        from zzpy import get_work_dir_path
        from zzpy import remove_dir
        from zzpy import get_file_name_list_from_dir
        import os

        tmp_dir = get_tmp_dir_path(root_dir=self.root_dir)
        work_dir = get_work_dir_path(root_dir=self.root_dir)

        self.assertFalse(os.path.exists(self.root_dir))
        init_dirs(root_dir=self.root_dir)
        self.assertTrue(os.path.exists(self.root_dir))
        self.assertTrue(os.path.exists(tmp_dir))
        self.assertTrue(os.path.exists(work_dir))

    def test_get_file_path_list_from_dir(self):
        from zzpy import get_file_path_list_from_dir
        from zzpy import write_file
        from zzpy import init_dir
        import os

        # init
        a_dir = os.path.join(self.root_dir, "a")
        aa_dir = os.path.join(a_dir, "aa")
        init_dir(aa_dir)
        a10_path = os.path.join(a_dir, "10.txt")
        write_file("10.txt", a10_path)
        aa11_path = os.path.join(aa_dir, "11.txt")
        write_file("11.txt", aa11_path)

        b_dir = os.path.join(self.root_dir, "b")
        bb_dir = os.path.join(b_dir, "bb")
        init_dir(bb_dir)
        bb20_path = os.path.join(bb_dir, "20.txt")
        write_file("20.txt", bb20_path)
        bb21_path = os.path.join(bb_dir, "21.txt")
        write_file("21.txt", bb21_path)

        c_dir = os.path.join(self.root_dir, "c")
        init_dir(c_dir)
        c30_path = os.path.join(c_dir, "30.txt")
        write_file("30.txt", c30_path)

        r_path = os.path.join(self.root_dir, "r.txt")
        write_file("r.txt", r_path)

        # test
        file_path_list = get_file_path_list_from_dir(
            self.root_dir)
        self.assertSetEqual(set(file_path_list), {
                            r_path, a10_path, aa11_path, bb20_path, bb21_path, c30_path})

    def test_get_file_name_list_from_dir(self):
        from zzpy import get_file_name_list_from_dir
        from zzpy import write_file
        from zzpy import init_dir
        import os

        # init
        a_dir = os.path.join(self.root_dir, "a")
        aa_dir = os.path.join(a_dir, "aa")
        init_dir(aa_dir)
        a10_path = os.path.join(a_dir, "10.txt")
        write_file("10.txt", a10_path)
        aa11_path = os.path.join(aa_dir, "11.txt")
        write_file("11.txt", aa11_path)

        b_dir = os.path.join(self.root_dir, "b")
        bb_dir = os.path.join(b_dir, "bb")
        init_dir(bb_dir)
        bb20_path = os.path.join(bb_dir, "20.txt")
        write_file("20.txt", bb20_path)
        bb21_path = os.path.join(bb_dir, "21.txt")
        write_file("21.txt", bb21_path)

        c_dir = os.path.join(self.root_dir, "c")
        init_dir(c_dir)
        c30_path = os.path.join(c_dir, "30.txt")
        write_file("30.txt", c30_path)

        r_path = os.path.join(self.root_dir, "r.txt")
        write_file("r.txt", r_path)

        # test
        file_path_list = get_file_name_list_from_dir(
            self.root_dir)
        self.assertSetEqual(set(file_path_list), {
                            "r.txt", "10.txt", "11.txt", "20.txt", "21.txt", "30.txt"})

    def test_get_file_line_count(self):
        from zzpy import get_file_line_count
        import os

        self.assertEqual(get_file_line_count(
            os.path.join("test", "static", "1.jsonl")), 2)
        self.assertEqual(get_file_line_count(
            os.path.join("test", "static", "2.jsonl")), 2)
        self.assertNotEqual(get_file_line_count(
            os.path.join("test", "static", "3.xls")), 0)
        self.assertNotEqual(get_file_line_count(
            os.path.join("test", "static", "4.xlsx")), 0)

    def test_get_tmp_dir_path(self):
        from zzpy import get_tmp_dir_path
        import os

        self.assertEqual(get_tmp_dir_path(), os.path.join("output", "tmp"))

    def test_get_work_dir_path(self):
        from zzpy import get_work_dir_path
        import os

        self.assertEqual(get_work_dir_path(), os.path.join("output", "work"))

    def test_write_file_and_read_file_when_dir_not_exist(self):
        from zzpy import write_file
        from zzpy import read_file
        from zzpy import read_bin_file
        import os

        write_content = "abc"
        self.assertFalse(os.path.exists(self.root_dir))
        file_path = os.path.join(self.root_dir, f"1.txt")
        write_file(content=write_content, file_path=file_path)
        self.assertTrue(os.path.exists(file_path))
        read_content = read_file(file_path)
        self.assertEqual(read_content, write_content)

    def test_write_file_and_read_file(self):
        from zzpy import write_file
        from zzpy import read_file
        from zzpy import read_bin_file
        import os

        # 校验当文件目录不存在时，是否可以写文件
        self.assertFalse(os.path.exists(self.root_dir))

        for i, write_content in enumerate(("abc", "你好", "abc你好", "你好abc", "こんにちは", "こんにちはzero", "zeroこんにちは", "你好zeroこんにちは", "こんにちはzero你好", "")):
            # default encoding
            file_path = os.path.join(self.root_dir, f"{i}-default.txt")
            write_file(content=write_content, file_path=file_path)
            self.assertTrue(os.path.exists(file_path))
            read_content = read_file(file_path)
            self.assertEqual(read_content, write_content)

            # encoding utf8
            file_path = os.path.join(self.root_dir, f"{i}-utf8.txt")
            write_file(content=write_content,
                       file_path=file_path, encoding="utf8")
            self.assertTrue(os.path.exists(file_path))
            read_content = read_file(file_path)
            self.assertEqual(read_content, write_content)

            # encoding gbk
            file_path = os.path.join(self.root_dir, f"{i}-gbk.txt")
            write_file(content=write_content,
                       file_path=file_path, encoding="gbk")
            self.assertTrue(os.path.exists(file_path))
            read_content = read_file(file_path)
            self.assertEqual(read_content, write_content)

    def test_get_one_file_path_from_dir_when_no_file(self):
        import os
        from zzpy import get_one_file_path_from_dir
        from zzpy import create_dir

        create_dir(os.path.join(self.root_dir, "empty-dir"))
        self.assertIsNone(get_one_file_path_from_dir(
            os.path.join(self.root_dir, "empty-dir")))

    def test_get_one_file_path_from_dir_when_single_file(self):
        import os
        from zzpy import write_file
        from zzpy import get_one_file_path_from_dir

        write_file("CONTENT", os.path.join(self.root_dir, "a", "a1.txt"))
        self.assertEqual(get_one_file_path_from_dir(os.path.join(self.root_dir, "a")), os.path.join(
            self.root_dir, "a", "a1.txt"))

    def test_get_one_file_path_from_dir_when_multi_files(self):
        import os
        from zzpy import write_file
        from zzpy import get_one_file_path_from_dir

        write_file("CONTENT", os.path.join(self.root_dir, "a", "a1.txt"))
        write_file("CONTENT", os.path.join(self.root_dir, "a", "a2.txt"))
        self.assertIn(get_one_file_path_from_dir(os.path.join(self.root_dir, "a")), (os.path.join(
            self.root_dir, "a", "a1.txt"), os.path.join(self.root_dir, "a", "a2.txt")))

    def test_get_one_file_path_from_dir_when_having_dirs_after_file(self):
        import os
        from zzpy import write_file
        from zzpy import get_one_file_path_from_dir

        write_file("CONTENT", os.path.join(self.root_dir, "c", "0.txt"))
        write_file("CONTENT", os.path.join(self.root_dir, "c", "3", "0.txt"))
        write_file("CONTENT", os.path.join(self.root_dir, "c", "1", "0.txt"))
        self.assertTrue(get_one_file_path_from_dir(os.path.join(
            self.root_dir, "c")), os.path.join(self.root_dir, "c", "0.txt"))

    def test_get_one_file_path_from_dir_when_having_dirs_before_file(self):
        import os
        from zzpy import write_file
        from zzpy import get_one_file_path_from_dir

        write_file("CONTENT", os.path.join(self.root_dir, "c", "4.txt"))
        write_file("CONTENT", os.path.join(self.root_dir, "c", "3", "0.txt"))
        write_file("CONTENT", os.path.join(self.root_dir, "c", "1", "0.txt"))
        self.assertTrue(get_one_file_path_from_dir(os.path.join(
            self.root_dir, "c")), os.path.join(self.root_dir, "c", "4.txt"))

    def test_move_file_from_src_dir_when_no_file_in_src(self):
        """当src没有文件时"""
        import os
        from zzpy import write_file
        from zzpy import get_file_path_list_from_dir
        from zzpy import move_file_from_src_dir

        move_file_from_src_dir(dst_file_path=os.path.join(self.root_dir,
                                                          "dst", "1.txt"), src_dir_path=os.path.join(self.root_dir, "src"))
        self.assertListEqual(get_file_path_list_from_dir(
            os.path.join(self.root_dir, "src")), [])
        self.assertListEqual(get_file_path_list_from_dir(
            os.path.join(self.root_dir, "dst")), [])

    def test_move_file_from_src_dir_when_single_in_src_and_dst_not_exist(self):
        """当src只有一个文件，dst不存在时"""
        import os
        from zzpy import write_file
        from zzpy import get_file_path_list_from_dir
        from zzpy import move_file_from_src_dir

        write_file("1", os.path.join(self.root_dir, "src", "1.txt"))
        move_file_from_src_dir(dst_file_path=os.path.join(self.root_dir,
                                                          "dst", "1.txt"), src_dir_path=os.path.join(self.root_dir, "src"))
        self.assertListEqual(get_file_path_list_from_dir(
            os.path.join(self.root_dir, "src")), [])
        self.assertListEqual(get_file_path_list_from_dir(os.path.join(self.root_dir, "dst")), [os.path.join(self.root_dir,
                                                                                                            "dst", "1.txt")])

    def test_move_file_from_src_dir_when_single_in_src_and_dst_empty(self):
        """当src只有一个文件，dst为空文件夹时"""
        import os
        from zzpy import write_file
        from zzpy import get_file_path_list_from_dir
        from zzpy import move_file_from_src_dir
        from zzpy import create_dir

        write_file("1", os.path.join(self.root_dir, "src", "1.txt"))
        create_dir(os.path.join(self.root_dir, "dst"))
        move_file_from_src_dir(dst_file_path=os.path.join(self.root_dir,
                                                          "dst", "1.txt"), src_dir_path=os.path.join(self.root_dir, "src"))
        self.assertListEqual(get_file_path_list_from_dir(
            os.path.join(self.root_dir, "src")), [])
        self.assertListEqual(get_file_path_list_from_dir(os.path.join(self.root_dir, "dst")), [os.path.join(self.root_dir,
                                                                                                            "dst", "1.txt")])

    def test_move_file_from_src_dir_when_single_in_src_and_dst_not_empty(self):
        """当src只有一个文件，dst不为空时"""
        import os
        from zzpy import write_file
        from zzpy import get_file_path_list_from_dir
        from zzpy import move_file_from_src_dir
        from zzpy import create_dir

        write_file("1", os.path.join(self.root_dir, "src", "1.txt"))
        write_file("2", os.path.join(self.root_dir, "dst", "2.txt"))
        move_file_from_src_dir(dst_file_path=os.path.join(self.root_dir,
                                                          "dst", "1.txt"), src_dir_path=os.path.join(self.root_dir, "src"))
        self.assertListEqual(get_file_path_list_from_dir(
            os.path.join(self.root_dir, "src")), [])
        self.assertListEqual(get_file_path_list_from_dir(os.path.join(self.root_dir, "dst")), [os.path.join(self.root_dir,
                                                                                                            "dst", "1.txt"), os.path.join(self.root_dir, "dst", "2.txt")])

    def test_move_file_from_src_dir_when_multi_in_src(self):
        """当src有多个文件时"""
        import os
        from zzpy import write_file
        from zzpy import get_file_path_list_from_dir
        from zzpy import move_file_from_src_dir
        from zzpy import create_dir

        write_file("1", os.path.join(self.root_dir, "src", "1.txt"))
        write_file("2", os.path.join(self.root_dir, "src", "2.txt"))
        write_file("2", os.path.join(self.root_dir, "dst", "3.txt"))
        move_file_from_src_dir(dst_file_path=os.path.join(self.root_dir,
                                                          "dst", "0.txt"), src_dir_path=os.path.join(self.root_dir, "src"))
        src_pathes = get_file_path_list_from_dir(
            os.path.join(self.root_dir, "src"))
        self.assertEqual(len(src_pathes), 1)
        self.assertIn(src_pathes[0], (os.path.join(
            self.root_dir, "src", "1.txt"), os.path.join(self.root_dir, "src", "2.txt")))
        dst_pathes = get_file_path_list_from_dir(
            os.path.join(self.root_dir, "dst"))
        self.assertEqual(len(dst_pathes), 2)
        self.assertListEqual(dst_pathes, [os.path.join(
            self.root_dir, "dst", "0.txt"), os.path.join(self.root_dir, "dst", "3.txt")])

    def test_move_file_from_src_dir_when_src_and_dst_have_same_file(self):
        """当src有多个文件时"""
        import os
        from zzpy import write_file
        from zzpy import get_file_path_list_from_dir
        from zzpy import move_file_from_src_dir
        from zzpy import read_file

        write_file("1", os.path.join(self.root_dir, "src", "1.txt"))
        write_file("2", os.path.join(self.root_dir, "dst", "1.txt"))
        move_file_from_src_dir(dst_file_path=os.path.join(self.root_dir,
                                                          "dst", "1.txt"), src_dir_path=os.path.join(self.root_dir, "src"))
        src_pathes = get_file_path_list_from_dir(
            os.path.join(self.root_dir, "src"))
        self.assertEqual(len(src_pathes), 0)

        dst_pathes = get_file_path_list_from_dir(
            os.path.join(self.root_dir, "dst"))
        self.assertEqual(len(dst_pathes), 1)
        dst_path = dst_pathes[0]
        self.assertEqual(dst_path, os.path.join(self.root_dir,
                                                "dst", "1.txt"))
        self.assertEqual(read_file(dst_path), "1")

    def test_normalize_path(self):
        import os
        from zzpy import windows_else
        from zzpy import normalize_path

        self.assertEqual(normalize_path(""), windows_else("", ""))

        self.assertEqual(normalize_path("."), windows_else(".", "."))
        self.assertEqual(normalize_path("./"), windows_else(".\\", "./"))
        self.assertEqual(normalize_path(".\\"), windows_else(".\\", "./"))
        self.assertEqual(normalize_path("./a"), windows_else(".\\a", "./a"))
        self.assertEqual(normalize_path(".\\a"), windows_else(".\\a", "./a"))

        self.assertEqual(normalize_path(".."), windows_else("..", ".."))
        self.assertEqual(normalize_path("../"), windows_else("..\\", "../"))
        self.assertEqual(normalize_path("..\\"), windows_else("..\\", "../"))
        self.assertEqual(normalize_path("../a"), windows_else("..\\a", "../a"))
        self.assertEqual(normalize_path("..\\a"),
                         windows_else("..\\a", "../a"))

        self.assertEqual(normalize_path("E:/a.txt"),
                         windows_else("E:a.txt", "E:/a.txt"))
        self.assertEqual(normalize_path("E:\\a.txt"),
                         windows_else("E:a.txt", "E:/a.txt"))

        self.assertEqual(normalize_path("E:/x/a.txt"),
                         windows_else("E:x\\a.txt", "E:/x/a.txt"))
        self.assertEqual(normalize_path("E:\\x\\a.txt"),
                         windows_else("E:x\\a.txt", "E:/x/a.txt"))

        self.assertEqual(normalize_path("/a.txt"),
                         windows_else("/a.txt", "/a.txt"))
        self.assertEqual(normalize_path("/x/a.txt"),
                         windows_else("/x\\a.txt", "/x/a.txt"))
