# tests/unit/test_file_operations.py
import unittest
from src.file_operations import load_words, save_words
import os

class TestFileOperations(unittest.TestCase):

    def setUp(self):
        # テスト用のデータを準備
        self.test_data = {"apple": {"meaning": "りんご", "mastery_level": 0}}
        self.test_filename = "test_words.csv"

    def test_load_words(self):
        # テスト用のファイルを作成
        with open(self.test_filename, "w") as file:
            file.write("apple,りんご,0\n")

        # 関数をテスト
        words = load_words(self.test_filename)
        self.assertEqual(words, self.test_data)

    def test_save_words(self):
        # 関数をテスト
        save_words(self.test_filename, self.test_data)

        # 保存された内容を確認
        with open(self.test_filename, "r") as file:
            content = file.read()
        self.assertEqual(content, "apple,りんご,0\n")

    def tearDown(self):
        # テスト用のファイルを削除
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

if __name__ == '__main__':
    unittest.main()
