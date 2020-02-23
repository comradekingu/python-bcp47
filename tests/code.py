
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
    with patch('bcp47.BCP47Code.construct') as m:
        lang_code = 'bcp47.BCP47Code.lang_code'
        with patch(lang_code, new_callable=PropertyMock) as m:
            m.return_value = "LANG CODE"
            code = BCP47Code(bcp, "foo", "bar", "baz")
            assert str(code) == "LANG CODE"
            assert (
                repr(code)
                == ("<%s.%s '%s' />"
                    % (code.__module__,
                       code.__class__.__name__,
                       code.lang_code)))


def test_bcp47_code_errors():
    bcp = BCP47()
    with patch('bcp47.BCP47Code.construct'):
        with patch('bcp47.BCP47Code.validate') as validate_m:
            validate_m.return_value = [23]
            code = BCP47Code(bcp)
            assert code._errors is None
            errors = code.errors
            assert errors == [23]
            assert code._errors == [23]
            assert code.errors == [23]
            # validate only called once
            assert (
                list(list(c) for c in validate_m.call_args_list)
                == [[(), {}]])


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
        errors = code.validate()
        assert errors == [23]
        assert (
            list(bcp.validate.call_args)
            == [(code, ), {}])


def test_bcp47_code_construct_from_kwargs():
    bcp = MagicMock()
    with patch('bcp47.BCP47Code.construct'):
        with patch('bcp47.BCP47Code._add_part') as m_add:
            m_add.side_effect = lambda parts, t, n: (
                parts.append(n) if n else None)
            code = BCP47Code(bcp)
            code.construct_from_kwargs(language="en", region="GB")
            assert (
                list(list(c[0][1:]) for c in m_add.call_args_list)
                == [['language', 'en'],
                    ['extlang', None],
                    ['script', None],
                    ['region', 'GB'],
                    ['variant', None]])
            assert code.errors is False
            assert (
                code.kwargs
                == {'language': 'en', 'region': 'GB'})
            assert code._lang_code == "en-GB"


def test_bcp47_code_props():
    bcp = BCP47()
    with patch('bcp47.BCP47Code.construct'):
        lang_code = 'bcp47.BCP47Code.lang_code'
        with patch(lang_code, new_callable=PropertyMock):
            code = BCP47Code(bcp)
            code.kwargs = {
                "language": "LANG",
                "extlang": "EXTLANG",
                "script": "SCRIPT",
                "region": "REGION",
                "variant": "VARIANT"}
            assert code.language == "LANG"
            assert code.extlang == "EXTLANG"
            assert code.script == "SCRIPT"
            assert code.region == "REGION"
            assert code.variant == "VARIANT"
