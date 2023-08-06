import re


def validate_function_app_name(function_app_name: str) -> bool:
    """

    Args:
        function_app_name:

    Returns:
        True is function_app_name is correct.

    See Also:
        https://docs.microsoft.com/ja-jp/azure/azure-functions/functions-create-first-azure-function#create-a-function-app
    """
    function_app_name_accept_pattern = r"^[A-Za-z0-9][A-Za-z0-9\-]+[A-Za-z0-9]$"
    result = re.match(function_app_name_accept_pattern, function_app_name)
    if result:
        return True
    return False
