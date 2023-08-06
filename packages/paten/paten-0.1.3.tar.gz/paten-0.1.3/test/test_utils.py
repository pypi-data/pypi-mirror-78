import pytest
from paten.utils import validate_function_app_name


@pytest.mark.parametrize("function_app_name", [
    "ABC-123",
    "abc-123",
])
def test_pass_function_app_name(function_app_name):
    assert validate_function_app_name(function_app_name=function_app_name)


@pytest.mark.parametrize("function_app_name", [
    "-ABC-123",
    "abc-123-",
    "ABC-#-123"
])
def test_error_function_app_name(function_app_name):
    assert not validate_function_app_name(function_app_name=function_app_name)
