"""
Help for webexport
"""

def add_arguments(parser):
    arg = parser.add_argument
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--dry-run', action='store_true', default=False,
                       help='dry run')
    arg('--json', metavar="FILE", help="write statistics to FILE")

def main(args):
    print(args)
