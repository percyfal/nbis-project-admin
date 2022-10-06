from nbis.cli import cli


def test_init_diary(runner, cd_tmp_path):
    result = runner.invoke(cli, ["diary"])
    print(result.stdout)
    print(result)
