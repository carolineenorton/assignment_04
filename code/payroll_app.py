import streamlit as st
from payroll import (
    load_employees,
    load_timesheet,
    build_payroll,
    payroll_export
)

st.title("Salt City Coffee – Weekly Payroll")
st.write("Upload the week's timesheet CSV to calculate payroll" +
        "and download the provider's file.")

roster = load_employees()

upload = st.file_uploader(
    "Upload timesheet CSV",
    type=["csv"],
    key="timesheet"
)

if upload is not None:
    timesheet = load_timesheet(upload)
    payroll = build_payroll(timesheet, roster)

    payroll_date = payroll["payroll_date"].iloc[0]
    st.subheader(f"Pay period: {payroll_date}")

    paid = payroll[payroll["pay_type"] != "unmatched"]
    overtime = payroll[payroll["pay_type"] == "overtime"]
    unmatched = payroll[payroll["pay_type"] == "unmatched"]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Employees paid", len(paid))

    with col2:
        st.metric("Total hours", payroll["hours_worked"].sum())

    with col3:
        st.metric("Total gross pay", f"${payroll['gross_pay'].sum():,.2f}")

    with col4:
        st.metric("Overtime weeks", len(overtime))

    if len(unmatched) > 0:
        employee_ids = ", ".join(unmatched["employee_id"].astype(str))
        st.warning(f"Unmatched employee IDs: {employee_ids}."
                   "Fix these before re-exporting."
                   )
    else:
        st.success("All employees matched the roster.")

    st.dataframe(payroll)

    st.download_button(
        label="Download payroll CSV",
        data=payroll_export(payroll).to_csv(index=False),
        file_name=f"payroll_{payroll_date}.csv",
        mime="text/csv",
        key="download"
    )
