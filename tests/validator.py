
from unittest.mock import MagicMock, patch

from bcp47 import BCP47Validator


def test_bcp47_validator_constructor():
    bcp = MagicMock()
    validator = BCP47Validator(bcp)
    assert validator.bcp47 is bcp


def test_bcp47_validate():
    bcp = MagicMock()

    with patch('bcp47.BCP47Validator.validate_regex') as reg_m:
        reg_m.return_value = reg_m.return_value = "FAIL"
        validator = BCP47Validator(bcp)
        validator.validate("asdf-asdf")
        assert (
            list(bcp.code_class.call_args)
            == [(bcp, ['asdf', 'asdf']), {}])
