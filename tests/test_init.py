from nbis.cli import cli


def test_init(runner, tmp_path):
    p = tmp_path / "project_foo"
    result = runner.invoke(cli, ["init", p])
    print(result)
