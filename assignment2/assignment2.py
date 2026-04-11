from __future__ import annotations

import csv
import os
import sys
import traceback
from datetime import datetime
from typing import Any

import custom_module


def _report(e: Exception) -> None:
    print("An exception occurred.", type(e).__name__)
    trace_back = traceback.extract_tb(e.__traceback__)
    stack_trace: list[str] = []
    for trace in trace_back:
        stack_trace.append(
            f"File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}"
        )
    print(f"Exception type: {type(e).__name__}")
    message = str(e)
    if message:
        print(f"Exception message: {message}")
    print(f"Stack trace: {stack_trace}")


# Task 2


def read_employees() -> dict[str, Any]:
    try:
        with open("../csv/employees.csv", newline="", encoding="utf-8") as handle:
            reader = csv.reader(handle)
            rows = list(reader)
        fields, *body = rows
        return {"fields": fields, "rows": body}
    except Exception as e:
        _report(e)
        sys.exit(1)


# Task 3


def column_index(name: str) -> int:
    return employees["fields"].index(name)


# Task 4


def first_name(row_number: int) -> str:
    idx = column_index("first_name")
    return employees["rows"][row_number][idx]


# Task 5


def employee_find(employee_id: int) -> list[list[str]]:
    def employee_match(row: list[str]) -> bool:
        return int(row[employee_id_column]) == employee_id

    return list(filter(employee_match, employees["rows"]))


# Task 6


def employee_find_2(employee_id: int) -> list[list[str]]:
    matches = list(
        filter(
            lambda row: int(row[employee_id_column]) == employee_id,
            employees["rows"],
        )
    )
    return matches


# Task 7


def sort_by_last_name() -> list[list[str]]:
    last_i = column_index("last_name")
    employees["rows"].sort(key=lambda row: row[last_i])
    return employees["rows"]


# Task 8


def employee_dict(row: list[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for field, value in zip(employees["fields"], row):
        if field == "employee_id":
            continue
        out[field] = value
    return out


# Task 9


def all_employees_dict() -> dict[str, dict[str, str]]:
    return {row[employee_id_column]: employee_dict(row) for row in employees["rows"]}


# Task 10


def get_this_value() -> str | None:
    return os.getenv("THISVALUE")


# Task 11


def set_that_secret(new_secret: str) -> None:
    custom_module.set_secret(new_secret)


# Task 12


def _read_minutes_file(path: str) -> dict[str, Any]:
    try:
        with open(path, newline="", encoding="utf-8") as handle:
            reader = csv.reader(handle)
            rows = list(reader)
        fields, *body = rows
        return {"fields": fields, "rows": [tuple(r) for r in body]}
    except Exception as e:
        _report(e)
        sys.exit(1)


def read_minutes() -> tuple[dict[str, Any], dict[str, Any]]:
    minutes_a = _read_minutes_file("../csv/minutes1.csv")
    minutes_b = _read_minutes_file("../csv/minutes2.csv")
    return minutes_a, minutes_b


# Task 13


def create_minutes_set() -> set[tuple[str, str]]:
    return set(minutes1["rows"]) | set(minutes2["rows"])


# Task 14


def create_minutes_list() -> list[tuple[str, datetime]]:
    as_list = list(minutes_set)
    return list(
        map(
            lambda item: (item[0], datetime.strptime(item[1], "%B %d, %Y")),
            as_list,
        )
    )


# Task 15


def write_sorted_list() -> list[tuple[str, str]]:
    minutes_list.sort(key=lambda item: item[1])
    as_strings = list(
        map(
            lambda item: (item[0], datetime.strftime(item[1], "%B %d, %Y")),
            minutes_list,
        )
    )
    with open("./minutes.csv", "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(minutes1["fields"])
        writer.writerows(as_strings)
    return as_strings


employees = read_employees()
print(employees)

employee_id_column = column_index("employee_id")

sort_by_last_name()
print(employees)

print(employee_dict(employees["rows"][0]))

print(all_employees_dict())

set_that_secret("notebook-seal")
print(custom_module.secret)

minutes1, minutes2 = read_minutes()
print(minutes1)
print(minutes2)

minutes_set = create_minutes_set()

minutes_list = create_minutes_list()
print(minutes_list)

print(write_sorted_list())
