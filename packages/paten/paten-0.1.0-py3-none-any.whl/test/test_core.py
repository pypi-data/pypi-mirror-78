import pytest

from paten import Paten
from paten.error import ArgumentNameInvalidError


def test_http_trigger():
    app = Paten("pytest")

    @app.http_trigger("req", methods=["GET"], route="/pytest")
    @app.out_queue("arg_name", queue_name="example-queue")
    @app.out_http()
    def example(req, arg_name):
        pass


def test_http_trigger_name_error():
    app = Paten("pytest")

    with pytest.raises(ArgumentNameInvalidError):
        @app.http_trigger("req", methods=["GET"], route="/pytest")
        @app.out_http()
        def example(req_different_name):
            pass

    with pytest.raises(ArgumentNameInvalidError):
        @app.http_trigger("req", methods=["GET"], route="/pytest")
        @app.out_queue("arg_name", queue_name="example-queue")
        @app.out_http()
        def example(req, arg_name_different):
            pass
