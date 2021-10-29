from mkcommit.include import include
import os
import unittest
import pyperclip
import shutil

from mkcommit.main import _main, Mode
from mkcommit.model import (
    CommaSeparatedList, ValidationFailedException, COMMIT_FUNC_NAME, PRE_COMMIT_FUNC_NAME
)
from mkcommit.include import DEFAULT_TEMP_PATH


class TestBasic(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.path = os.path.join(
            os.path.dirname(__file__),
            '..',
            'res',
            'example.test.mkcommit.py'
        )
        cls.path_hook = os.path.join(
            os.path.dirname(__file__),
            '..',
            'res',
            'example.hook.mkcommit.py'
        )

    def test_basic_file_config_stdout(self):
        """Test whether STDOUT write works properly"""
        stdout_writes = []
        clipboard_writes = []

        _main(
            self.path,
            Mode.STDOUT,
            None,
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

    def test_hook_valid(self):
        try:
            _main(
                self.path_hook,
                Mode.HOOK,
                "KrCz | blah"
            )
        except ValidationFailedException:
            self.fail()

    def test_hook_invalid(self):
        with self.assertRaises(ValidationFailedException):
            _main(
                self.path_hook,
                Mode.HOOK,
                "KrCz | asdf"
            )

    def test_include(self):
        url = "https://raw.githubusercontent.com/" + \
              "kjczarne/mkcommit/master/test/res/example.semantic.mkcommit.py"
        url2 = "https://raw.githubusercontent.com/" + \
               "kjczarne/mkcommit/master/test/res/example.hook.mkcommit.py"
        commit, on_commit = include(url)
        commit2, on_commit2 = include(url2, "temp.mkcommit.py")
        if on_commit is None or on_commit2 is None:
            self.fail(f"`{PRE_COMMIT_FUNC_NAME}` was `None`")
        else:
            self.assertEqual(commit.__name__, COMMIT_FUNC_NAME)
            self.assertEqual(on_commit.__name__, PRE_COMMIT_FUNC_NAME)
            self.assertEqual(commit2.__name__, COMMIT_FUNC_NAME)
            self.assertEqual(on_commit2.__name__, PRE_COMMIT_FUNC_NAME)
        if not os.path.exists(os.path.join(DEFAULT_TEMP_PATH, "temp.mkcommit.py")):
            self.fail("`include` call with named tempfile failed")

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(DEFAULT_TEMP_PATH)


if __name__ == "__main__":
    unittest.main()
