import os
import unittest
import pyperclip

from mkcommit.main import _main, Mode
from mkcommit.model import CommaSeparatedList


class TestBasic(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.path = os.path.join(
            os.path.dirname(__file__),
            '..',
            'res',
            'example.test.mkcommit.py'
        )

    def test_basic_file_config_stdout(self):
        """Test whether STDOUT write works properly"""
        stdout_writes = []
        clipboard_writes = []

        _main(
            self.path,
            Mode.STDOUT,
            lambda msg: stdout_writes.append(msg),
            lambda msg: clipboard_writes.append(msg)
        )

        self.assertEqual(len(clipboard_writes), 0)
        self.assertEqual(len(stdout_writes), 1)

    def test_basic_file_config_clipboard(self):
        """Test whether Clipboard write works properly"""
        _main(
            self.path,
            Mode.CLIPBOARD
        )
        msg = pyperclip.paste()
        self.assertEqual("[MYPROJECT-1234/KrCz] feat: cool", msg)
    
    def test_comma_separated_list_with_spaces(self):
        """Tests yes-space comma separated list"""
        with_spaces = CommaSeparatedList("eins", "zwei", "drei")
        self.assertEqual(str(with_spaces), "eins, zwei, drei")

    def test_comma_separated_list_no_spaces(self):
        """Tests no-space comma separated list"""
        no_spaces = CommaSeparatedList("eins", "zwei", "drei", no_space=True)
        self.assertEqual(str(no_spaces), "eins,zwei,drei")


if __name__ == "__main__":
    unittest.main()
