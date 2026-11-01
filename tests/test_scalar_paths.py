import pytest

from dotty_dict import Dotty, dotty


@pytest.mark.parametrize('value', [0, 1, 1.5, False, True])
def test_get_returns_default_below_scalar(value):
    data = dotty({'outer': {'scalar': value}})
    sentinel = object()
    assert data.get('outer.scalar.child', sentinel) is sentinel
    assert data['outer.scalar'] == value
    with pytest.raises(KeyError):
        data['outer.scalar.child']


def test_scalar_missing_path_with_custom_separator():
    data = Dotty({'outer': {'scalar': 1}}, separator='/')
    assert data.get('outer/scalar/child', 'missing') == 'missing'


def test_none_intermediate_retains_existing_behavior():
    data = dotty({'outer': None})
    assert data.get('outer.child', 'default') is None
