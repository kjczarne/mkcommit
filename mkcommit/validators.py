from mkcommit.model import Validator
import re


def matches(pattern: str) -> Validator:
    def _v(msg: str) -> bool:
        """Checks if the input matches a RegEx pattern"""
        if re.match(pattern, msg):
            return True
        else:
            return False
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


def max_len(limit: int) -> Validator:
    def _v(msg: str) -> bool:
        """Checks if the input exceeds maximum length"""
        if len(msg) > limit:
            return False
        else:
            return True
    return _v
