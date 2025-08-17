import unittest
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from functions.run_python import run_python_file


class TestGetFilesInfo(unittest.TestCase):
    def test_calculator_dir(self):
        result = get_files_info("calculator", ".")
        # print(result)
        self.assertTrue("Result for current directory:" in result)
        self.assertTrue(" - main.py: file_size=576 bytes, is_dir=False" in result)
        self.assertTrue(" - tests.py: file_size=1343 bytes, is_dir=False" in result)
        self.assertTrue(" - pkg: file_size=92 bytes, is_dir=True" in result)

    def test_calculator_pkg(self):
        result = get_files_info("calculator", "pkg")
        # print(result)
        self.assertTrue("Result for 'pkg' directory:" in result)
        self.assertTrue(
            " - calculator.py: file_size=1739 bytes, is_dir=False" in result
        )
        self.assertTrue(" - render.py: file_size=768 bytes, is_dir=False" in result)

    def test_calculator_bin(self):
        result = get_files_info("calculator", "/bin")
        # print(result)
        self.assertTrue("Result for '/bin' directory:" in result)
        self.assertTrue(
            '    Error: Cannot list "/bin" as it is outside the permitted working directory'
            in result
        )

    def test_calculator_back(self):
        result = get_files_info("calculator", "../")
        # print(result)
        self.assertTrue("Result for '../' directory:" in result)
        self.assertTrue(
            '    Error: Cannot list "../" as it is outside the permitted working directory'
            in result
        )


class TestGetFileContent(unittest.TestCase):
    def test_main(self):
        result = get_file_content("calculator", "main.py")
        # print(result)
        self.assertTrue("def main():" in result)

    def test_pkg_calculator(self):
        result = get_file_content("calculator", "pkg/calculator.py")
        # print(result)
        self.assertTrue("def _apply_operator(self, operators, values)" in result)

    def test_bin_cat(self):
        result = get_file_content("calculator", "/bin/cat")
        # print(result)
        self.assertTrue("Error: " in result)

    def test_pkg_does_not_exist(self):
        result = get_file_content("calculator", "pkg/does_not_exist.py")
        # print(result)
        self.assertTrue("Error: " in result)


class TestWriteFile(unittest.TestCase):
    def test_calculator_lorem(self):
        result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        # print(result)
        self.assertEqual(
            'Successfully wrote to "lorem.txt" (28 characters written)', result
        )

    def test_calculator_more_lorem(self):
        result = write_file(
            "calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"
        )
        # print(result)
        self.assertEqual(
            'Successfully wrote to "pkg/morelorem.txt" (26 characters written)', result
        )

    def test_tmp(self):
        result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        # print(result)
        self.assertTrue("Error: " in result)


class TestRunPython(unittest.TestCase):
    def test_calculator_main(self):
        result = run_python_file("calculator", "main.py")
        # print(result)
        self.assertTrue("Calculator App" in result)
        self.assertTrue('Usage: python main.py "<expression>"' in result)
        self.assertTrue('Example: python main.py "3 + 5"' in result)

    def test_calculator_main_3p5(self):
        result = run_python_file("calculator", "main.py", ["3 + 5"])
        # print(result)
        self.assertTrue("3 + 5" in result)
        self.assertTrue("=" in result)
        self.assertTrue("8" in result)

    def test_calculator_outside_err(self):
        result = run_python_file("calculator", "tests.py")
        # print(result)
        self.assertTrue("Ran 9 tests in " in result)
        self.assertTrue("OK" in result)

    def test_calculator_nonexistent(self):
        result = run_python_file("calculator", "../main.py")
        # print(result)
        self.assertTrue("Error:" in result)

    def test_calculator_lorem(self):
        result = run_python_file("calculator", "nonexistent.py")
        # print(result)
        self.assertTrue("Error:" in result)


if __name__ == "__main__":
    unittest.main()
