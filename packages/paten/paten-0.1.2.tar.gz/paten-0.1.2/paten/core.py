from inspect import signature
import json
import os
from shutil import copyfile, copytree, rmtree
from typing import Union, Optional

from .error import ArgumentNameInvalidError
from .binding import (
    BindingManager,
    Binding
)


class Paten:

    def __init__(self, function_app_name: str, module_folder_list: Optional[list] = None):
        """
        set function-app-name for the Azure Functions.
        
        Args:
            function_app_name: A name for the Azure Functions to deploy.
        
        """
        # function app candidate to deploy to.
        self.function_app_name = function_app_name
        # user-defined module folder list
        self.module_folder_list = ["shared_code"]
        if module_folder_list:
            self.module_folder_list.extend(module_folder_list)
        # manage user-define-handlers to generate `function.json` with bindings
        self.binding_manager = BindingManager()

    @staticmethod
    def _check_argument(function: callable, arg_name: str) -> None:
        """
        Check whether the `arg_name` in the parameter of the `function`.
        
        Args:
            function: function to check
            arg_name: argument name
        
        Raises:
            ArgumentNameInvalidError: When `arg_name` is not found in the paramater of the `function`
        
        """
        # check arguments
        sig = signature(function)
        if arg_name not in sig.parameters:
            raise ArgumentNameInvalidError(f"{arg_name} not in {function.__name__}")

    def trigger(self, name: str, _type: str, **kwargs):
        """
        Add Trigger.

        Args:
            name: A name for the argument.
            _type: A name for the trigger type.
            **kwargs: Required parameters in each trigger type.

        Returns:

        """
        def _wrapper(function):
            self._check_argument(function=function, arg_name=name)

            handler_name = str(function.__name__)
            self.binding_manager.register_binding(
                Binding(
                    handler_name=handler_name,
                    name=name,
                    _type=_type,
                    direction="in",
                    **kwargs
                )
            )
            self.binding_manager.register_function_app(handler_name=handler_name)
            return function

        return _wrapper

    def http_trigger(self, name: str, methods: Union[list, str], route: str, auth_level: str = "function"):
        """
        Add HttpTrigger.
        
        Args:
            name: A name for the argument, usually `req`.
            methods: Accepted method name.
            route: Route name for the Function App.
            auth_level: Authentication level for the Function App, function, anonymous are acceptable.
        
        """
        return self.trigger(
            name=name,
            _type="httpTrigger",
            route=route,
            methods=methods,
            authLevel=auth_level
        )

    def timer_trigger(self, name: str, schedule: str):
        """
        Add TimerTrigger.
        
        Args:
            name: A name for the argument, usually `timer`.
            schedule: The time when the Function App is invoked.
        
        """
        return self.trigger(
            name=name,
            _type="timerTrigger",
            schedule=schedule
        )

    def queue_trigger(self, name: str, queue_name: str, connection: Optional[str] = None):
        """
        Add QueueTrigger.
        
        Args:
            name: A name for the argument, usually `msg`.
            queue_name: A name for the Queue Storage where the `msg` enqueue or dequeue.
            connection: A connection for the Queue Storage, by default `AzureWebJobsStorage`.
        
        """
        return self.trigger(
            name=name,
            _type="queueTrigger",
            queueName=queue_name,
            connection=connection if connection is not None else "AzureWebJobsStorage"
        )

    def blob_trigger(self, name: str, path: str, connection: Optional[str] = None):
        """
        Add BlobTrigger.
        
        Args:
            name: A name for the argument, usually `blob`.
            path: A path for the Blob Storage to invoke the Function App.
            connection: A connection for the Blob Storage, by default `AzureWebJobsStorage`.
        
        """
        return self.trigger(
            name=name,
            _type="blobTrigger",
            path=path,
            connection=connection if connection is not None else "AzureWebJobsStorage"
        )

    def in_bind(self, name: str, _type: str, **kwargs):
        """
        Add in-bind.

        Args:
            name: A name for the argument.
            _type: A name for the trigger type.
            **kwargs: Required parameters in each trigger type.

        Returns:

        """
        def _wrapper(function):
            handler_name = str(function.__name__)
            self.binding_manager.register_binding(
                Binding(
                    handler_name=handler_name,
                    name=name,
                    _type=_type,
                    direction="in",
                    **kwargs
                )
            )
            return function

        return _wrapper

    def out_bind(self, name: str, _type: str, is_arg_name_check: bool = True, **kwargs):
        """

        Args:
            name: A name for the argument.
            _type: A name for the trigger type.
            is_arg_name_check: if True, check the argument-name of the function.
            **kwargs: Required parameters in each trigger type.

        Returns:

        """
        def _wrapper(function):
            if is_arg_name_check:
                self._check_argument(function=function, arg_name=name)
            handler_name = str(function.__name__)
            self.binding_manager.register_binding(
                Binding(
                    handler_name=handler_name,
                    name=name,
                    _type=_type,
                    direction="out",
                    **kwargs
                )
            )
            return function

        return _wrapper

    def out_http(self, name: Optional[str] = "$return"):
        return self.out_bind(name=name, _type="http", is_arg_name_check=False)

    def out_queue(self, name: str, queue_name: str, connection: Optional[str] = None):
        return self.out_bind(
            name=name,
            _type="queue",
            queueName=queue_name,
            connection=connection if connection is not None else "AzureWebJobsStorage"
        )

    @staticmethod
    def _generate_function_json():
        return {
            "scriptFile": "__init__.py"
        }

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
        """
        Export files required for deploying Azure Functions.
        Export directory is `./.paten`.
        
        """
        file_parent_dir = f"./.paten"
        # clean file_parent_dir before creating files
        rmtree(file_parent_dir)
        os.makedirs(file_parent_dir, exist_ok=True)

        # copy requirements.txt
        copyfile("requirements.txt", f"{file_parent_dir}/requirements.txt")

        with open(f"{file_parent_dir}/proxies.json", "w") as f:
            json.dump(self._generate_proxies_json(), f)

        with open(f"{file_parent_dir}/local.settings.json", "w") as f:
            json.dump(self._generate_local_settings_json(), f)

        with open(f"{file_parent_dir}/host.json", "w") as f:
            json.dump(self._generate_host_json(), f)

        for func in self.binding_manager.function_app_list:
            function_app_dir = f"{file_parent_dir}/{func['function_name']}"
            os.makedirs(function_app_dir, exist_ok=True)

            # function.jsonの取得と配置
            out: dict = func['function_json']
            with open(f'{function_app_dir}/function.json', 'w') as f:
                json.dump(out, f)

            # 関数ファイルの配置
            copyfile("app.py", f"{function_app_dir}/__init__.py")

        # copy user-defined module folders
        for folder in self.module_folder_list:
            if os.path.isdir(folder):
                copytree(folder, f"{file_parent_dir}/{folder}")

    def plan(self) -> list:
        """
        Display function app to deploy.
        
        """
        output_list = ["app.py", "|"]
        for func in self.binding_manager.function_app_list:
            output_list.append(f"|-{func['function_name']}")
            for bindings in func['function_json']['bindings']:
                output_list.append(f"|  |-[{bindings['type']}] {bindings['name']}")
            output_list.append("|")

        return output_list
