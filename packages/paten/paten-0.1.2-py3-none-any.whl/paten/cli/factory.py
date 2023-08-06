import importlib
import subprocess
import sys

from paten import Paten
from paten.error import AzureFunctionsCoreToolsNotFoundError


class CliFactory:

    def __init__(self, function_app_dir: str):
        self.function_app_dir = function_app_dir

    def load_paten_app(self) -> Paten:
        if self.function_app_dir not in sys.path:
            sys.path.insert(0, self.function_app_dir)
        try:
            app = importlib.import_module('app')
            paten_app = getattr(app, 'app')
        except SyntaxError as e:
            message = (
                          'Unable to import your app.py file:\n\n'
                          'File "%s", line %s\n'
                          '  %s\n'
                          'SyntaxError: %s'
                      ) % (getattr(e, 'filename'), e.lineno, e.text, e.msg)
            raise RuntimeError(message)
        return paten_app

    @staticmethod
    def _check_required_library_installed():
        """
        `which` command returns 127, if specified command not found.

        Returns:
            None

        Raises:
            AzureFunctionsCoreToolsNotFoundError
        """
        check_command = ["which", "az"]
        try:
            _ = subprocess.run(
                check_command,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except subprocess.CalledProcessError:
            raise AzureFunctionsCoreToolsNotFoundError("`Azure CLI` is not found.")

        check_command = ["which", "func"]
        try:
            _ = subprocess.run(
                check_command,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except subprocess.CalledProcessError:
            raise AzureFunctionsCoreToolsNotFoundError("`Azure Functions Core Tools` is not found.")

    def deploy(self, prompter, function_app_name: str):
        prompter.echo(f"deploy start at {self.function_app_dir}")
        deploy_command = ["func", "azure", "functionapp", "publish", function_app_name]

        try:
            self._check_required_library_installed()

            _ = subprocess.run(
                deploy_command,
                cwd=".paten",
                check=True)
        except subprocess.CalledProcessError as e:
            prompter.echo(e)
            stdout = e.stdout.decode()
            if stdout:
                prompter.echo(stdout)
            stderr = e.stderr.decode()
            if stderr:
                prompter.echo(stderr)

        except AzureFunctionsCoreToolsNotFoundError as e:
            prompter.echo(e)
