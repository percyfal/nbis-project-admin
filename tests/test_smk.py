from nbis.cli import cli


expected_init = [
    "project_foo/pyproject.toml",
    "project_foo/src/nbis-admin/snakemake/config.py",
    "project_foo/config/local/config.yaml",
    "project_foo/config/config.yaml",
    "project_foo/schemas/config.schema.yaml",
    "project_foo/schemas/samples.schema.yaml",
    "project_foo/resources/samples.tsv",
]


expected_add = [
    "project_foo/pyproject.toml",
    "project_foo/src/snakemake/commands/smk-run.smk",
    "project_foo/src/nbis-admin/commands/smk.py",
]


def test_smk_init(runner, pyproject):
    out = pyproject
    result = runner.invoke(cli, ["smk", "init"])
    files = [str(p.relative_to(out.parent)) for p in out.rglob("*") if p.is_file()]
    assert not result.exception
    assert sorted(files) == sorted(expected_init)


def test_smk_add(runner, pyproject):
    out = pyproject
    config = out / "src" / "nbis-admin" / "snakemake" / "config.py"
    config.parent.mkdir(parents=True)
    config.touch()
    result = runner.invoke(cli, ["smk", "add"])
    config.unlink()
    files = [str(p.relative_to(out.parent)) for p in out.rglob("*") if p.is_file()]
    assert not result.exception
    assert sorted(files) == sorted(expected_add)
