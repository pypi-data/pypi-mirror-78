"""
Classes to mange bindings for `function.json`.

"""
from enum import Enum, auto
import re

from .error import BindingInvalidError, DecoratorAdditionInvalidError


class BindingType(Enum):
    TRIGGER = auto()
    IN = auto()
    OUT = auto()

    @staticmethod
    def get_type(_type: str, direction: str):
        # if `_type` contains `Trigger`, return TRIGGER
        trigger_bind = "[a-z]*Trigger"
        result = re.match(trigger_bind, _type)
        if result:
            return BindingType.TRIGGER

        # else, according to the `direction`
        if direction == "in":
            return BindingType.IN
        elif direction == "out":
            return BindingType.OUT
        else:
            raise BindingInvalidError(f"[{_type}] and [{direction}] are not matched.")


class Binding:
    """
    Mange simple one binding.

    """

    def __init__(self, handler_name: str, name: str, _type: str, direction: str, **kwargs):
        self.handler_name = handler_name
        self.name = name
        self.type = _type
        self.direction = direction
        self.kwargs = kwargs
        self.bind_type = BindingType.get_type(_type=_type, direction=direction)

    def to_dict(self):
        bind_info = {
            "name": self.name,
            "type": self.type,
            "direction": self.direction
        }
        bind_info.update(self.kwargs)

        return bind_info


class BindingManager:
    """
    Manage bindings and function list to generate `function.json`
    
    Example:
        >>> binding_manager = BindingManager()
        >>> binding = Binding(handler_name="some_function", name="req", _type="httpTrigger", direction="in")
        >>> binding_manager.register_binding(binding)
    
    """
    def __init__(self):
        # manage function list including bindings
        self.function_app_list = []
        # manage bindings
        self.binding_list = []

    def _check_trigger_exists(self, handler_name: str) -> bool:
        handler_name_related_bind = [bind.bind_type for bind in self.binding_list if bind.handler_name == handler_name]
        if BindingType.TRIGGER in handler_name_related_bind:
            return True
        return False

    def register_binding(self, binding: Binding):
        if self._check_trigger_exists(handler_name=binding.handler_name):
            raise DecoratorAdditionInvalidError("cannot add @out/@in-binding after @trigger-binding.")
        self.binding_list.append(binding)

    def register_function_app(self, handler_name: str):
        function_app_dict = self.get_binding_by_handler_name(handler_name)
        self.function_app_list.append(function_app_dict)

    def get_binding_by_handler_name(self, handler_name: str) -> dict:
        return {
            "function_name": handler_name,
            "function_json": {
                "scriptFile": "__init__.py",
                "entryPoint": handler_name,
                "bindings": [bind.to_dict() for bind in self.binding_list if
                             bind.handler_name == handler_name]
            }
        }
