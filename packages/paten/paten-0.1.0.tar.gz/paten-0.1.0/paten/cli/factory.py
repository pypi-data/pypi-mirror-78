import importlib
import sys

from paten import Paten


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
