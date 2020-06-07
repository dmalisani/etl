import csv


def reader(filepath: str, delimiter=",", encoding="latin-1"):
    with open(filepath, "r", encoding=encoding) as rows:
        for row in csv.reader(rows):
            yield row
