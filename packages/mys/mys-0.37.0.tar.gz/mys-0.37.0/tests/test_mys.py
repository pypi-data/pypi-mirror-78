import sys
import unittest
from mys.transpile import transpile

from .utils import read_file

class MysTest(unittest.TestCase):

    maxDiff = None

    def assert_equal_to_file(self, actual, expected):
        # open(expected, 'w').write(actual)
        self.assertEqual(actual, read_file(expected))

    def test_all(self):
        datas = [
            'basics',
            'calc',
            'hello_world',
            'loops',
            'strings',
            'various'
        ]

        for data in datas:
            self.assert_equal_to_file(
                transpile(read_file(f'tests/files/{data}.mys')),
                f'tests/files/{data}.mys.cpp')

    def test_invalid_main_argument(self):
        with self.assertRaises(Exception) as cm:
            transpile('def main(args: int): pass')

        self.assertEqual(str(cm.exception),
                         "main() takes 'args: [str]' or no arguments.")

    def test_invalid_main_return_type(self):
        with self.assertRaises(Exception) as cm:
            transpile('def main() -> int: pass')

        self.assertEqual(str(cm.exception), "main() must return 'None'.")

    def test_lambda_not_supported(self):
        with self.assertRaises(Exception) as cm:
            transpile('def main(): print((lambda x: x)(1))', 'foo.py')

        self.assertEqual(str(cm.exception),
                         '  File "foo.py", line 1\n'
                         '    def main(): print((lambda x: x)(1))\n'
                         '                       ^\n'
                         'LanguageError: lambda functions are not supported')

    def test_bad_syntax(self):
        with self.assertRaises(Exception) as cm:
            transpile('DEF main(): pass')

        if sys.version_info < (3, 8):
            return

        self.assertEqual(str(cm.exception),
                         '  File "<unknown>", line 1\n'
                         '    DEF main(): pass\n'
                         '        ^\n'
                         'SyntaxError: invalid syntax')
