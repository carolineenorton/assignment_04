"""
compute.py — Step 3 of the pipeline: pay, labels, and the file the provider wants.

Two element functions that need **two** values from a row, two DataFrame
functions that run them across every row with `DataFrame.apply(..., axis=1)`,
the function that chains all three steps into one call, and the export that
reshapes the result for the online payroll provider.

No walkthrough this time. You have `clean.py` and `join.py` beside you, the
docstrings say what each function must return, and `tests/test_unit.py` and
`tests/test_pipeline.py` say exactly how they will be checked.
"""

import pandas as pd

from .clean import add_hourly_rate, add_hours_worked
from .join import merge_employees

OVERTIME_THRESHOLD = 40.0   # weekly hours above this are paid at time-and-a-half
OVERTIME_MULTIPLIER = 1.5


def calc_gross_pay(hours: float, rate: float) -> float:
    """Return the gross pay for a week of work, given hours and hourly rate."""
    if pd.isna(rate):
        return 0.0
    if hours <= OVERTIME_THRESHOLD:
        return round(hours * rate, 2)
    else:
        regular_pay = OVERTIME_THRESHOLD * rate
        overtime_hours = hours - OVERTIME_THRESHOLD
        overtime_pay = overtime_hours * rate * OVERTIME_MULTIPLIER
        return round(regular_pay + overtime_pay, 2)


def classify_pay(hours: float, rate: float) -> str:
    """Return a string label for the type of pay."""
    if pd.isna(rate):
        return "unmatched"
    if hours > OVERTIME_THRESHOLD:
        return "overtime"
    return "regular"


def add_gross_pay(payroll: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of `payroll` with one new column, `gross_pay` (float)."""
    out = payroll.copy()
    out["gross_pay"] = out.apply(
        lambda row: calc_gross_pay(row["hours_worked"], row["hourly_rate_usd"]),
        axis=1
    )
    return out


def add_pay_type(payroll: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of `payroll` with one new column, `pay_type` (string)."""
    out = payroll.copy()
    out["pay_type"] = out.apply(
        lambda row: classify_pay(row["hours_worked"], row["hourly_rate_usd"]),
        axis=1
    )
    return out


def build_payroll(timesheet: pd.DataFrame, employees: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with all the payroll columns, ready for export."""
    cleaned_timesheet = add_hours_worked(timesheet)
    cleaned_employees = add_hourly_rate(employees)
    merged = merge_employees(cleaned_timesheet, cleaned_employees)
    with_gross_pay = add_gross_pay(merged)
    final_payroll = add_pay_type(with_gross_pay)
    return final_payroll


def payroll_export(payroll: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of `payroll` with only the columns the provider wants, renamed."""
    export = payroll[payroll["pay_type"] != "unmatched"].copy()
    export = export[["payroll_date", "employee_id", "hours_worked", "hourly_rate_usd",
                    "gross_pay"]]
    export.columns = ["payrolldate", "employeeid", "hours", "rate", "total"]
    return export
