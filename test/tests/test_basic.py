import os
import unittest
import pyperclip

from mkcommit.main import _main, Mode


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
        _main(
            self.path,
            Mode.CLIPBOARD
        )
        msg = pyperclip.paste()
        self.assertEqual("[MYPROJECT-1234/KrCz] feat: cool", msg)


if __name__ == "__main__":
    unittest.main()
