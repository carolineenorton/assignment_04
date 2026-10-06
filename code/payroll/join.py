"""
join.py — Step 2 of the pipeline: bring the roster onto the timesheet.

The timesheet knows *who worked and how long*. The roster knows *what each
person is paid*. Neither file can produce a paycheck on its own, so the pipeline
has to combine them — and the two files have different **grains**: one row per
week-of-work versus one row per person. That is exactly what `pd.merge` is for.

The decision in this step is not *how* to merge but *which kind*. Read the
docstring before you pick `how=`.

Less scaffolding here: the steps are described, the code is yours.
"""

import pandas as pd


def merge_employees(timesheet: pd.DataFrame, employees: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of `timesheet` with the roster's columns added, one row per"""
    merged = pd.merge(timesheet, employees, how="left", on="employee_id")
    return merged
