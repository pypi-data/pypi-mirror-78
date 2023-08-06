class PatenBaseError(Exception):
    pass


class ArgumentNameInvalidError(PatenBaseError):
    pass


class BindingInvalidError(PatenBaseError):
    pass


class DecoratorAdditionInvalidError(PatenBaseError):
    pass


class AzureFunctionsCoreToolsNotFoundError(PatenBaseError):
    pass
