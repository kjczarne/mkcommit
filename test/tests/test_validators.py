import unittest
import re

from mkcommit.fixtures import _ask
from mkcommit.model import CommitMessage
from mkcommit.validators import max_len, matches, is_int, is_float


class TestValidators(unittest.TestCase):

    def make_valid(self):
        integer = _ask("Integer Test", check=is_int())
        floating_point = _ask("Float Test", check=is_float())
        some_regex = _ask("Regex Test", check=matches(r'match_me'))
        max_length = _ask("Max Length Test", check=max_len(30))

        c_valid = CommitMessage(
            f"{integer}-{floating_point}-{some_regex}-{max_length}",
            ""
        )

        return c_valid

    def make_invalid(self):
        integer = _ask("Integer Test Invalid", check=is_int())
        floating_point = _ask("Float Test Invalid", check=is_float())
        some_regex = _ask("Regex Test Invalid", check=matches(r'match_me'))
        max_length = _ask("Max Length Test Invalid", check=max_len(30))

        c_invalid = CommitMessage(
            f"{integer}-{floating_point}-{some_regex}-{max_length}",
            ""
        )

        return c_invalid
    
    def test_validators_valid(self):
        """Correctly validated fixture should have no invalid text"""
        msg = self.make_valid().first_line
        invalid_bits = re.findall(r'INVALID', msg)
        self.assertEqual(0, len(invalid_bits))
    
    def test_validators_invalid(self):
        """Each invalid input should properly add `INVALID-` fixture prefix."""
        msg = self.make_invalid().first_line
        invalid_bits = re.findall(r'INVALID', msg)
        self.assertEqual(4, len(invalid_bits))

if __name__ == "__main__":
    unittest.main()
