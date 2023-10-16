from precommit_recommendations.__main__ import main

from click.testing import CliRunner


def test_precommit_recommendations_cli():
    runner = CliRunner()
    result = runner.invoke(main, ())
    assert result.exit_code == 0
