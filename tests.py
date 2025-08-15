import unittest
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info


class TestGetFilesInfo(unittest.TestCase):
    def test_calculator_dir(self):
        result = get_files_info("calculator", ".")
        print(result)
        self.assertEqual(
            result,
            """Result for current directory:
 - main.py: file_size=576 bytes, is_dir=False
 - tests.py: file_size=1343 bytes, is_dir=False
 - pkg: file_size=66 bytes, is_dir=True""",
            # - pkg: file_size=92 bytes, is_dir=True""",
        )

    def test_calculator_pkg(self):
        result = get_files_info("calculator", "pkg")
        print(result)
        self.assertEqual(
            result,
            """Result for 'pkg' directory:
 - calculator.py: file_size=1739 bytes, is_dir=False
 - render.py: file_size=768 bytes, is_dir=False""",
        )

    def test_calculator_bin(self):
        result = get_files_info("calculator", "/bin")
        print(result)
        self.assertEqual(
            result,
            """Result for '/bin' directory:
    Error: Cannot list "/bin" as it is outside the permitted working directory""",
        )

    def test_calculator_back(self):
        result = get_files_info("calculator", "../")
        print(result)
        self.assertEqual(
            result,
            """Result for '../' directory:
    Error: Cannot list "../" as it is outside the permitted working directory""",
        )


class TestGetFileContent(unittest.TestCase):
    def test_main(self):
        result = get_file_content("calculator", "main.py")
        print(result)
        self.assertTrue("def main():" in result)

    def test_pkg_calculator(self):
        result = get_file_content("calculator", "pkg/calculator.py")
        print(result)
        self.assertTrue("def _apply_operator(self, operators, values)" in result)

    def test_bin_cat(self):
        result = get_file_content("calculator", "/bin/cat")
        print(result)
        self.assertTrue("Error: " in result)

    def test_pkg_does_not_exist(self):
        result = get_file_content("calculator", "pkg/does_not_exist.py")
        print(result)
        self.assertTrue("Error: " in result)


if __name__ == "__main__":
    unittest.main()
