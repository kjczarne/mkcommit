from typing import Callable, List
from mkcommit.model import ValidationFailedException
import unittest
from mkcommit.suites import semantic
from mkcommit.suites import conventional
from mkcommit.suites import technica


class Fixture(unittest.TestCase):

    def eval_list(self, valid: List[str], invalid: List[str], validator: Callable[[str], bool]):
        for c in valid:
            try:
                validator(c)
            except ValidationFailedException:
                self.fail(
                    f"Validation failed on `{c}` although it's listed as a valid input."
                )
        for c in invalid:
            msg = f"`{c}` is listed as an invalid input but was validated as correct."
            with self.assertRaises(ValidationFailedException, msg=msg):
                validator(c)


class TestSemantic(Fixture):

    @classmethod
    def setUpClass(cls) -> None:
        cls.semantic_valid = [
            "feat(scope): badsfasdf",
            "feat: asdfadsfasdf",
            "feat, fix: adfsasdfas",
            "feat,fix: asdfasdfasdf",
            "feat(asdf),fix(asda),feat, fix(asda): asdfasdfasdf",
            "feat,fix!: asdfasdfasdf",
            "Merge branch a into b",
            "Merge branch chore/123/something into develop",
        ]
        cls.semantic_invalid = [
            "asdf(blah): adsf",
            "asdf,feat(blah): asdf",
            "asdfa, feat(blah): asdfg",
            "feat,fix?: asdfasdfasdf",
        ]
        cls.semantic_valid_msg_len = ["feat: asdfasdf"]
        cls.semantic_invalid_msg_len = ["feat: " + "a" * 56]

    def test_semantic(self):
        self.eval_list(
            self.semantic_valid,
            self.semantic_invalid,
            semantic.is_semantic
        )

    def test_semantic_msg_len(self):
        self.eval_list(
            self.semantic_valid_msg_len,
            self.semantic_invalid_msg_len,
            semantic.has_short_commit_msg_proper_length
        )


class TestConventional(Fixture):

    @classmethod
    def setUpClass(cls) -> None:
        cls.conventional_valid = [
            "feat(scope): badsfasdf",
            "feat: asdfadsfasdf",
            "feat(scope)!: badsfasdf",
            "feat!: asdfadsfasdf",
            "Merge branch a into b",
            "Merge branch chore/123/something into develop",
        ]
        cls.conventional_invalid = [
            "asdf(blah): adsf",
            "asdf,feat(blah): asdf",
            "asdfa, feat(blah): asdfg",
            "feat,fix?: asdfasdfasdf",
            "feat, fix: adfsasdfas",
            "feat,fix: asdfasdfasdf",
            "feat(asdf),fix(asda),feat, fix(asda): asdfasdfasdf",
            "feat,fix!: asdfasdfasdf",
            "feat(blah has space): adsf",
        ]

    def test_conventional(self):
        self.eval_list(
            self.conventional_valid,
            self.conventional_invalid,
            conventional.is_conventional
        )


class TestTechnica(Fixture):

    @classmethod
    def setUpClass(cls) -> None:
        cls.technica_valid = [
            "[KrCz/PROJECT-1234] feat: asdfads",
            "[KrCz/PROJECT-1234] feat, fix: asdfads",
            "[KrCz/PROJECT-1234] feat,fix(context): asdfads",
            "[KrCz/PROJECT-1234] feat(context), fix(context): asdfads",
            "[KrCz/PROJECT-1234]feat,fix(context): asdfads",
            "[KrCz/project-1234] feat,fix(context): asdfads",
            "[KrCz/---] feat: lol",
            "[KrCz/-] feat: lol",
            "Merge branch a into b",
            "Merge branch chore/123/something into develop",
        ]
        cls.technica_invalid = [
            "[KrCZ/PROJECT-1234] feat,fix(context): asdfads",
            "[KrCz/PROJECT1234] feat: asdfads",
            "[KrCz/PROJECT-1234] asdf: asdfads",
            "[KrCz/PROJECT-1234] asdf,fix: asdfads",
            "KrCz/PROJECT-1234 feat: asdfads",
            "[KrCz\\PROJECT-1234] chore: asdfads",
            "[KrCz/--] feat: lol",
            "[KrCz/] feat: lol",
        ]

    def test_technica(self):
        self.eval_list(
            self.technica_valid,
            self.technica_invalid,
            technica.is_technica
        )


if __name__ == "__main__":
    unittest.main()
