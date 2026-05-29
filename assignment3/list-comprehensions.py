# Task 3

import csv


def main() -> None:
    with open("../csv/employees.csv", newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))

    if len(rows) < 2:
        raise ValueError("employees.csv needs a header row and at least one data row")

    header, *data_rows = rows
    first_i = header.index("first_name")
    last_i = header.index("last_name")

    names = [f"{row[first_i]} {row[last_i]}" for row in data_rows]
    print(names)

    with_e = [name for name in names if "e" in name]
    print(with_e)


if __name__ == "__main__":
    main()
