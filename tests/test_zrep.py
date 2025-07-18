#!/usr/bin/env python3

import os
import shutil
import tempfile
import unittest

from zrep.zrep import ZRep, check_pattern_in_file, is_binary_file, replace_in_file


class TestZRep(unittest.TestCase):
    """测试ZRep类"""

    def setUp(self):
        """设置测试环境"""
        self.test_dir = tempfile.mkdtemp()
        self.zrep = ZRep()

    def tearDown(self):
        """清理测试环境"""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def create_test_file(self, filename: str, content: str) -> str:
        """创建测试文件"""
        filepath = os.path.join(self.test_dir, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return filepath

    def test_get_file_paths(self):
        """测试文件路径获取"""
        # 创建测试文件
        self.create_test_file("test1.txt", "hello world")
        self.create_test_file("subdir/test2.py", 'print("hello")')
        self.create_test_file("subdir/test3.js", 'console.log("hello")')

        # 创建应该被排除的目录
        os.makedirs(os.path.join(self.test_dir, ".git"), exist_ok=True)
        self.create_test_file(".git/config", "git config")

        file_paths = self.zrep.get_file_paths(self.test_dir)

        # 验证结果
        self.assertEqual(len(file_paths), 3)
        self.assertTrue(any("test1.txt" in path for path in file_paths))
        self.assertTrue(any("test2.py" in path for path in file_paths))
        self.assertTrue(any("test3.js" in path for path in file_paths))
        self.assertFalse(any(".git" in path for path in file_paths))

    def test_replace_in_directory(self):
        """测试目录中的字符串替换"""
        # 创建测试文件
        file1 = self.create_test_file("test1.txt", "hello world\nhello python")
        file2 = self.create_test_file("test2.py", 'print("hello")\nprint("goodbye")')

        # 执行替换
        count = self.zrep.replace_in_directory(self.test_dir, "hello", "hi")

        # 验证结果
        self.assertEqual(count, 2)

        # 检查文件内容
        with open(file1, encoding="utf-8") as f:
            content1 = f.read()
        self.assertEqual(content1, "hi world\nhi python")

        with open(file2, encoding="utf-8") as f:
            content2 = f.read()
        self.assertEqual(content2, 'print("hi")\nprint("goodbye")')


class TestUtilityFunctions(unittest.TestCase):
    """测试工具函数"""

    def setUp(self):
        """设置测试环境"""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """清理测试环境"""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def create_test_file(self, filename: str, content: str, mode: str = "w") -> str:
        """创建测试文件"""
        filepath = os.path.join(self.test_dir, filename)
        with open(filepath, mode, encoding="utf-8" if mode == "w" else None) as f:
            f.write(content)
        return filepath

    def test_is_binary_file(self):
        """测试二进制文件检测"""
        # 创建文本文件
        text_file = self.create_test_file("test.txt", "hello world")
        self.assertFalse(is_binary_file(text_file))

        # 创建二进制文件
        binary_file = self.create_test_file("test.bin", b"\x00\x01\x02\x03", "wb")
        self.assertTrue(is_binary_file(binary_file))

    def test_check_pattern_in_file(self):
        """测试文件中模式检查"""
        # 创建测试文件
        test_file = self.create_test_file("test.txt", "hello world\nfoo bar")

        # 测试存在的模式
        self.assertTrue(check_pattern_in_file(test_file, "hello"))
        self.assertTrue(check_pattern_in_file(test_file, "world"))
        self.assertTrue(check_pattern_in_file(test_file, "foo bar"))

        # 测试不存在的模式
        self.assertFalse(check_pattern_in_file(test_file, "goodbye"))
        self.assertFalse(check_pattern_in_file(test_file, "python"))

    def test_replace_in_file(self):
        """测试文件中的字符串替换"""
        # 创建测试文件
        test_file = self.create_test_file("test.txt", "hello world\nhello python")

        # 执行替换
        result = replace_in_file(test_file, "hello", "hi")
        self.assertTrue(result)

        # 检查文件内容
        with open(test_file, encoding="utf-8") as f:
            content = f.read()
        self.assertEqual(content, "hi world\nhi python")

        # 测试不存在的模式
        result = replace_in_file(test_file, "goodbye", "bye")
        self.assertFalse(result)

    def test_replace_in_binary_file(self):
        """测试二进制文件不被替换"""
        # 创建二进制文件
        binary_file = self.create_test_file("test.bin", b"\x00hello\x01world\x02", "wb")

        # 尝试替换
        result = replace_in_file(binary_file, "hello", "hi")
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
