import csv


def append_row(path, row):
    with open(path, "a", newline="") as handle:
        csv.writer(handle).writerow(row)
