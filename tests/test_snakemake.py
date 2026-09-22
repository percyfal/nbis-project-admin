"""Test snakemake module."""

import click

from nbis.snakemake import (
    no_profile_option,
    profile_option,
    report_option,
    snakemake_argument_list,
    test_option,
)


def test_snakemake_args(runner):
    """Test snakemake args."""

    @click.command(context_settings={"ignore_unknown_options": True})
    @profile_option()
    @snakemake_argument_list()
    def cmd(profile, snakemake_args):
        print(profile, list(snakemake_args))

    ret = runner.invoke(cmd, [])
    assert ret.stdout == "['--profile', 'local'] []\n"
    ret = runner.invoke(cmd, ["--dry-run", "--printshellcmds"])
    assert ret.stdout == "['--profile', 'local'] ['--dry-run', '--printshellcmds']\n"


class TestProfileOption:
    """Test snakemake profile_option."""

    def test_profile_option(self, runner):
        """Test profile_option."""

        @click.command()
        @profile_option()
        def cmd(profile):
            print(profile)

        ret = runner.invoke(cmd, [])
        assert ret.stdout == "['--profile', 'local']\n"
        ret = runner.invoke(cmd, ["--profile", "test"])
        assert ret.stdout == "['--profile', 'test']\n"

    def test_no_profile_option(self, runner):
        """Test no_profile_option."""

        @click.command()
        @profile_option()
        @no_profile_option()
        def cmd(profile, no_profile):  # pylint: disable=unused-argument
            print(profile)

        ret = runner.invoke(cmd, [])
        assert ret.stdout == "['--profile', 'local']\n"
        ret = runner.invoke(cmd, ["--no-profile"])
        assert ret.stdout == "[]\n"


class TestReportOption:
    """Test snakemake report_option."""

    def test_report_option(self, runner):
        """Test report_option."""

        @click.command()
        @report_option()
        def cmd(report):
            print(report)

        ret = runner.invoke(cmd, [])
        assert ret.stdout == "[]\n"
        ret = runner.invoke(cmd, ["--report"])
        assert ret.stdout == "['--report', 'report.html']\n"

    def test_report_option_with_profile(self, runner):
        """Test report option with profile."""

        @click.command()
        @report_option(report_file="test.html")
        @profile_option()
        @no_profile_option()
        def cmd(report, profile, no_profile):  # pylint: disable=unused-argument
            print(report, profile)

        ret = runner.invoke(cmd, [])
        assert ret.stdout == "[] ['--profile', 'local']\n"
        ret = runner.invoke(cmd, ["--report"])
        assert ret.stdout == "['--report', 'test.html'] []\n"


class TestTestOption:
    """Test snakemake test_option."""

    def test_test_option(self, runner):
        """Test test_option."""

        @click.command()
        @test_option()
        def cmd(test):
            print(test)

        ret = runner.invoke(cmd, [])
        assert ret.stdout == "[]\n"
        ret = runner.invoke(cmd, ["--test"])
        assert ret.stdout == "['--config', '__test__=True']\n"

    def test_test_option_with_config(self, runner):
        """Test test_option with config."""

        @click.command()
        @test_option(config=["foo=bar"])
        def cmd(test):
            print(test)

        ret = runner.invoke(cmd, ["--test"])
        assert ret.stdout == "['--config', '__test__=True', 'foo=bar']\n"

    def test_test_option_with_options(self, runner):
        """Test test_option with options."""

        @click.command()
        @test_option(options=["--foo", "bar"])
        def cmd(test):
            print(test)

        ret = runner.invoke(cmd, ["--test"])
        assert ret.stdout == "['--foo', 'bar', '--config', '__test__=True']\n"
