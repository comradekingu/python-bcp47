

from bcp47 import BCP47Validator


def test_bcp47_validate_regex():
    validator = BCP47Validator(None)
    assert validator.validate_regex("asdf-asdf") is None
