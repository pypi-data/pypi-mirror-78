from click.testing import CliRunner

from paten.cli import (
    plan
)

runner = CliRunner()


def test_plan_error():
    result = runner.invoke(plan)
    assert result.exit_code == 1
