
from unittest.mock import MagicMock, PropertyMock, patch

import pytest

from bcp47 import BCP47, BCP47Code


def test_bcp47_code_args_and_kwargs():
    bcp = BCP47()
    with pytest.raises(Exception) as e:
        BCP47Code(bcp, "foo", "bar", "baz", foo="foo0")
    assert e.value.args[0].startswith("Mixture of args and kwargs")


def test_bcp47_code_no_args_or_kwargs():
    bcp = BCP47()
    with pytest.raises(Exception) as e:
        BCP47Code(bcp)
    assert e.value.args[0].startswith("No arguments provided")


def test_bcp47_code_args():
    bcp = BCP47()
    with patch('bcp47.BCP47Code.construct') as m:
        BCP47Code(bcp, "foo", "bar", "baz")
        assert (
            list(m.call_args)
            == [('foo', 'bar', 'baz'), {}])


def test_bcp47_code_kwargs():
    bcp = BCP47()
    with patch('bcp47.BCP47Code.construct') as m:
        BCP47Code(bcp, foo="foo0", bar="bar0", baz="baz0")
        assert (
            list(m.call_args)
            == [(), {'foo': 'foo0', 'bar': 'bar0', 'baz': 'baz0'}])


def test_bcp47_code_string():
    bcp = BCP47()
    with patch('bcp47.BCP47Code.lang_code', new_callable=PropertyMock) as m:
        m.return_value = "LANG CODE"
        code = BCP47Code(bcp, "foo", "bar", "baz")
        assert str(code) == "LANG CODE"


def test_bcp47_code_errors():
    bcp = BCP47()
    with patch('bcp47.BCP47Code.construct'):
        lang_code = 'bcp47.BCP47Code.lang_code'
        with patch(lang_code, new_callable=PropertyMock) as lang_m:
            with patch('bcp47.BCP47Code.validate') as validate_m:
                validate_m.return_value = [23]
                lang_m.return_value = 'LANG CODE'
                code = BCP47Code(bcp)
                assert code._errors is None
                errors = code.errors
                assert errors == [23]
                assert code._errors == [23]
                assert code.errors == [23]
                assert (
                    list(list(c) for c in validate_m.call_args_list)
                    == [[('LANG CODE',), {}]])


def test_bcp47_code_valid():
    bcp = BCP47()
    with patch('bcp47.BCP47Code.construct'):
        errors = 'bcp47.BCP47Code.errors'
        with patch(errors, new_callable=PropertyMock) as error_m:
            code = BCP47Code(bcp)
            error_m.return_value = [23]
            assert not code.valid
            error_m.return_value = None
            assert code.valid


def test_bcp47_code_validate():
    bcp = MagicMock()
    with patch('bcp47.BCP47Code.construct'):
        bcp.validate.return_value = [23]
        code = BCP47Code(bcp)
        errors = code.validate(7)
        assert errors == [23]
        assert (
            list(bcp.validate.call_args)
            == [(7,), {}])
