"""Module defining commonly used cli arguments."""


def add_dry_run(parser):
    parser.add_argument(
        "--dry-run", "-n", action="store_true", default=False, help="dry run"
    )


def add_output_file(parser):
    parser.add_argument(
        "--output-file",
        action="store",
        required=True,
        help="output file",
    )
