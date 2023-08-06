import argparse
import sys

from csv2tsv import to_tsv


def main():
    parser = argparse.ArgumentParser(description="convert csv file to tsv file.")

    parser.add_argument("src", help="input file/dir path.")
    parser.add_argument("-o", "--output", help="output dir path.", metavar="\b")
    parser.add_argument(
        "-e",
        "--encoding",
        default="utf-8",
        help="open file with encoding.",
        metavar="\b",
    )
    parser.add_argument(
        "-d", "--delimiter", default=",", help="delimiter of src csv.", metavar="\b",
    )

    args = parser.parse_args()

    to_tsv(args.src, args.output, encoding=args.encoding, delimiter=args.delimiter)


if __name__ == "__main__":
    if not len(args := sys.argv) > 1:
        sys.argv.append("-h")
    main()
