import pytest

from paten import Paten
from paten.error import (
    ArgumentNameInvalidError,
    DecoratorAdditionInvalidError
)


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


def test_timer_trigger():
    app = Paten("pytest")

    @app.timer_trigger("timer", schedule="0 0 19 * * *")
    def example(timer):
        pass


def test_timer_trigger_name_error():
    app = Paten("pytest")

    with pytest.raises(ArgumentNameInvalidError):
        @app.timer_trigger("timer", schedule="0 0 19 * * *")
        def example(timer_name_different):
            pass


def test_queue_trigger():
    app = Paten("pytest")

    @app.queue_trigger("msg", queue_name="example-queue")
    def example(msg):
        pass


def test_queue_trigger_name_error():
    app = Paten("pytest")

    with pytest.raises(ArgumentNameInvalidError):
        @app.queue_trigger("msg", queue_name="example-queue")
        def example(msg_name_different):
            pass


def test_blob_trigger():
    app = Paten("pytest")

    @app.blob_trigger("blob", path="example/test.csv")
    def example(blob):
        pass


def test_blob_trigger_name_error():
    app = Paten("pytest")

    with pytest.raises(ArgumentNameInvalidError):
        @app.blob_trigger("blob", path="example/test.csv")
        def example(blob_name_different):
            pass


def test_decorator_addition_error():
    app = Paten("paten")

    with pytest.raises(DecoratorAdditionInvalidError):
        @app.out_http()
        @app.http_trigger(name="req", methods=["POST"], route="/test")
        def example(req):
            pass
