#!/usr/bin/env python3

import csv
from argparse import ArgumentParser


def main(args):
    # Read the rows of the CSV file into a list.
    with open(args.csv_file, "r") as f:
        reader = csv.reader(f, delimiter=args.csv_delimiter)
        rows = list(reader)

    # If there are no rows, then there's nothing we need to do.
    if len(rows) == 0:
        return

    # Verify that all rows have the same number of columns.
    n_columns = len(rows[0])
    for i, row in enumerate(rows):
        if len(row) != n_columns:
            raise ValueError(f"Wrong number of columns in row {i}.")

    # Compute the padded width of each column.
    widths = [max([len(s) for s in column]) for column in zip(*rows)]

    # Print the LaTeX version of the table.
    for i, row in enumerate(rows):
        padded = [s.ljust(width) for s, width in zip(row, widths)]
        print(" & ".join(padded) + r" \\", end="")
        border = args.first_border if not i else args.other_border
        print(" " + border if (border and i < len(rows) - 1) else "")


def parse_args():
    parser = ArgumentParser()

    # Required arguments
    parser.add_argument(
        "csv_file", help="the CSV file whose contents should be converted to a LaTeX table"
    )

    # Optional arguments
    parser.add_argument("-c", "--csv-delimiter", default=",", help="the CSV item delimiter")
    parser.add_argument(
        "-f", "--first-border", default="", help="the LaTeX command to add after the first row"
    )
    parser.add_argument(
        "-o",
        "--other-border",
        default="",
        help="the LaTeX command to add after rows other than the first",
    )

    return parser.parse_args()


if __name__ == "__main__":
    main(parse_args())
