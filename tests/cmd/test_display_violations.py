import io
from multiprocessing.sharedctypes import Value
import unittest

from typing import Iterator
from unittest.mock import patch
from parameterized import parameterized

from yamler.cmd import ERR
from yamler.cmd import SUCCESS
from yamler.cmd import display_violations
from yamler.cmd import DisplayMethod
from yamler.violations import RequiredViolation, ViolationType


class TestDisplayViolations(unittest.TestCase):
    @parameterized.expand([
        ('display_table_with_violations',
            [RequiredViolation("data", "-")], DisplayMethod.TABLE, ERR),
        ('display_table_without_violations', [], DisplayMethod.TABLE, SUCCESS),
        ('display_json_with_violations',
            [RequiredViolation("data", "-")], DisplayMethod.JSON, ERR),
        ('display_json_without_violations', [], DisplayMethod.JSON, SUCCESS),
    ])
    def test_display_violations(self, name, violations: Iterator[ViolationType],
                                display_method: str, expected_status_code: int):
        # Suppress the print statements
        with patch('sys.stdout', new=io.StringIO()):
            status_code = display_violations(violations, display_method)
            self.assertEqual(expected_status_code, status_code)

    @parameterized.expand([
        ('with_none_violations', None, DisplayMethod.JSON),
        ('with_none_display_method', [RequiredViolation("data", "-")], None),
        ('with_violations_and_display_method_none', None, None)
    ])
    def test_display_violations_invalid_params(self, name,
                                               violations: Iterator[ViolationType],
                                               display_method: str):
        with self.assertRaises(ValueError):
            display_violations(violations, display_method)


if __name__ == '__main__':
    unittest.main()