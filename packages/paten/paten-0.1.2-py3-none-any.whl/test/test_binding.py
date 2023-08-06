import pytest

from paten.binding import BindingType
from paten.error import BindingInvalidError


def test_binding_invalid_error():
    with pytest.raises(BindingInvalidError):
        BindingType.get_type("queue", "not_in")
