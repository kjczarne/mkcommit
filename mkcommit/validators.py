from mkcommit.model import Validator
import re


def matches(pattern: str) -> Validator:
    def _v(msg: str) -> bool:
        """Checks if the input matches a RegEx pattern"""
        if re.match(pattern, msg):
            return True
        else:
            return False
    _v.__doc__ = f"The pattern {pattern} hasn't been matched to the input"
    return _v


def is_int() -> Validator:
    def _v(msg: str) -> bool:
        """Checks if the input is an integer"""
        return matches(r'^\d+$')(msg)
    return _v


def is_float() -> Validator:
    def _v(msg: str) -> bool:
        """Checks if the input is a float"""
        return matches(r'^\d+\.\d+$|^\d+$')(msg)
    return _v


def min_len(limit: int) -> Validator:
    def _v(msg: str) -> bool:
        """Checks if the input is at least `limit` characters long"""
        return len(msg) >= limit
    return _v


def max_len(limit: int) -> Validator:
    def _v(msg: str) -> bool:
        """Checks if the input exceeds maximum length"""
        return len(msg) < limit
    return _v


def validate_initials(
    first_name_chars: int,
    last_name_chars: int,
    verbose: bool = False
) -> Validator:
    def _v(msg: str) -> bool:
        tot = str(first_name_chars + last_name_chars)
        if not matches(r"\w{" + tot + r"}")(msg):
            return False
        else:
            if not msg[0].isupper():
                if verbose:
                    print("Fist letter of the first name not uppercase!")
                return False
            if not msg[1:first_name_chars].islower():
                if verbose:
                    print("Letters of the first name not lowercase!")
                return False
            if not msg[0 + first_name_chars].isupper():
                if verbose:
                    print("First letter of the last name not uppercase!")
                return False
            if not msg[first_name_chars + 1:first_name_chars + last_name_chars].islower():
                if verbose:
                    print("Letters of the last name not lowercase!")
                return False
            if not len(msg) == first_name_chars + last_name_chars:
                return False
            return True
    _v.__doc__ = f"""Initials should be {first_name_chars + last_name_chars}-letter
words with {first_name_chars} letters of your first name
and {last_name_chars} letters of your last name.
"""
    return _v


def is_true() -> Validator:
    def _v(msg: str) -> bool:
        if msg:
            return True
        else:
            return False
    _v.__doc__ = "Was `False`, expected `True`"
    return _v


def is_false() -> Validator:
    def _v(msg: str) -> bool:
        return not is_true()(msg)
    _v.__doc__ = "Was `True`, expected `False`"
    return _v


def are_keywords_selected() -> Validator:
    def _v(msg: str) -> bool:
        """Checks if at least one keyword has been selected."""
        return min_len(1)(msg)
    _v.__doc__ = """No keywords have been selected. This is not allowed.
 Use `chore` for generic tasks."""
    return _v
