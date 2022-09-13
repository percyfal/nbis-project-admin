# NB: For some reason cannot invoke the top-level cli group when
# defined by add_command
def test_init_diary(main, runner, cd_tmp_path):
    res = runner.invoke(main.commands["diary"], [])
    print(res.stdout)
    print(res)
