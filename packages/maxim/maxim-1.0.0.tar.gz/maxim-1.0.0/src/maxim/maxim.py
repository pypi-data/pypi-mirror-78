import argparse

from .sub_maxim import get_maxim

__version__ = "1.0.0"


def main():

    parser = argparse.ArgumentParser(
        prog="maxim",
        description="""Simple wrapper to fortune module.""",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s " + __version__,
        help="print version information",
    )

    parser.add_argument(
        "-f",
        "--fortune-file",
        dest="fortune_file",
        default="/usr/share/games/fortunes/fortunes",
        help="fortune program’s text file. (default %(default)s)",
    )

    args = parser.parse_args()

    print(get_maxim(args.fortune_file))
