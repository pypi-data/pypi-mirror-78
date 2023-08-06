from inspect import signature
import json
import os
from typing import Union, Optional
from shutil import copyfile

from .error import ArgumentNameInvalidError


class Paten:

    def __init__(self, function_app_name: str, requirements: Optional[list] = None):
        self.function_app_name = function_app_name
        # manage function list including bindings
        self.function_info_list = []
        # manage bindings
        self.function_bind_list = []
        # requirements
        self.requirements = requirements

    def http_trigger(self, name, methods: Union[list, str], route: str, auth_level: str = "function"):
        def _wrapper(function):
            # check arguments
            sig = signature(function)
            if name not in sig.parameters:
                raise ArgumentNameInvalidError(f"{name} not in {function.__name__}")

            self.function_bind_list.append({
                "function_name": str(function.__name__),
                "values": {
                    "authLevel": auth_level,
                    "type": "httpTrigger",
                    "direction": "in",
                    "name": name,
                    "route": route,
                    "methods": methods
                }
            })

            self.function_info_list.append({
                "function_name": str(function.__name__),
                "function_json": {
                    "scriptFile": "__init__.py",
                    "entryPoint": str(function.__name__),
                    "bindings": [d['values'] for d in self.function_bind_list if
                                 d['function_name'] == str(function.__name__)]
                }
            })
            return function
        return _wrapper

    def out_http(self, name: Optional[str] = None):
        def _wrapper(function):
            _name = name if name is not None else "$return"

            self.function_bind_list.append({
                "function_name": str(function.__name__),
                "values": {
                    "type": "http",
                    "direction": "out",
                    "name": _name
                }
            })
            return function
        return _wrapper

    def out_queue(self, name: str, queue_name: str, connection: Optional[str] = None):
        def _wrapper(function):
            # check arguments
            sig = signature(function)
            if name not in sig.parameters:
                raise ArgumentNameInvalidError(f"{name} not in {function.__name__}")

            _connection = connection if connection is not None else "AzureWebJobsStorage"

            self.function_bind_list.append({
                "function_name": str(function.__name__),
                "values": {
                    "type": "queue",
                    "direction": "out",
                    "name": name,
                    "queueName": queue_name,
                    "connection": _connection
                }
            })
            return function
        return _wrapper

    @staticmethod
    def _generate_function_json():
        return {
            "scriptFile": "__init__.py"
        }

    def _generate_requirements_txt(self) -> list:
        if self.requirements is None:
            return []
        return self.requirements

    @staticmethod
    def _generate_host_json() -> dict:
        return {
            "version": "2.0",
            "extensionBundle": {
                "id": "Microsoft.Azure.Functions.ExtensionBundle",
                "version": "[1.*, 2.0.0)"
            }
        }

    @staticmethod
    def _generate_local_settings_json() -> dict:
        return {
            "IsEncrypted": False,
            "Values": {
                "AzureWebJobsStorage": "",
                "FUNCTIONS_WORKER_RUNTIME": "python"
            }
        }

    @staticmethod
    def _generate_proxies_json() -> dict:
        return {
            "$schema": "http://json.schemastore.org/proxies",
            "proxies": {}
        }

    def export(self):
        output_dir = f"./.paten"
        os.makedirs(output_dir, exist_ok=True)

        # requirementsファイルの複製
        copyfile("requirements.txt", f"./.paten/requirements.txt")

        with open("./.paten/proxies.json", "w") as f:
            json.dump(self._generate_proxies_json(), f)

        with open("./.paten/local.settings.json", "w") as f:
            json.dump(self._generate_local_settings_json(), f)

        with open("./.paten/host.json", "w") as f:
            json.dump(self._generate_host_json(), f)

        with open("./.paten/requirements.txt", mode='w') as f:
            f.writelines('\n'.join(self._generate_requirements_txt()))

        for func in self.function_info_list:
            output_dir = f"./.paten/{func['function_name']}"
            os.makedirs(output_dir, exist_ok=True)

            # function.jsonの取得と配置
            out: dict = func['function_json']
            with open(f'{output_dir}/function.json', 'w') as f:
                json.dump(out, f)

            # 関数ファイルの配置
            copyfile("app.py", f"{output_dir}/__init__.py")

    def plan(self) -> list:
        output_list = ["app.py", "|"]
        for func in self.function_info_list:
            output_list.append(f"|-{func['function_name']}")
            for bindings in func['function_json']['bindings']:
                output_list.append(f"|  |-[{bindings['type']}] {bindings['name']}")
            output_list.append("|")

        return output_list
