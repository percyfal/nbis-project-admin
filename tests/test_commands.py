def test_init_diary(main, runner, cd_tmp_path):
    _ = runner.invoke(main, ["diary", "init", "-d", "foo"])
