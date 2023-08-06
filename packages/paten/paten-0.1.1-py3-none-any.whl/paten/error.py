class PatenBaseError(Exception):
    pass


class ArgumentNameInvalidError(PatenBaseError):
    pass


class AzureFunctionsCoreToolsNotFoundError(PatenBaseError):
    pass
