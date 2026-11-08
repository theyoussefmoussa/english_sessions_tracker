"""Class roll-call tab: take attendance for many students at once."""
from datetime import date

import psycopg
import streamlit as st

from src.attendance_service import (
    DatabaseConnectionError,
    get_active_students,
    get_attendance_for_date,
    save_bulk_attendance,
)
from utils.constants import GRADES

STATUS_OPTIONS = ["Present", "Absent"]
DEFAULT_STATUS = "Absent"  # everyone starts Absent; mark who came


def render_roll_call():
    st.subheader("Take attendance for a class")

    try:
        students = get_active_students()  # [(username, full_name, grade), ...]
    except DatabaseConnectionError as e:
        st.error(str(e))
        return
    except psycopg.Error as e:
        st.error(f"Database error: {e}")
        return

    if not students:
        st.info("No active students found.")
        return

    # Grade and date sit OUTSIDE the form: they decide which students are
    # listed and which saved statuses get pre-filled.
    col_grade, col_date = st.columns(2)
    grade_choice = col_grade.selectbox("Grade", ["All grades", *GRADES])
    attendance_date = col_date.date_input(
        "Date", value=date.today(), key="roll_call_date"
    )

    shown = [s for s in students if grade_choice == "All grades" or s[2] == grade_choice]
    if not shown:
        st.info(f"No active students in {grade_choice}.")
        return

    try:
        saved = get_attendance_for_date(attendance_date)
    except DatabaseConnectionError as e:
        st.error(str(e))
        return
    except psycopg.Error as e:
        st.error(f"Database error: {e}")
        return

    recorded = sum(1 for username, _, _ in shown if username in saved)
    st.caption(f"{recorded} of {len(shown)} students already recorded for {attendance_date}.")

    with st.form("roll_call_form"):
        selections = {}
        for username, full_name, grade in shown:
            default = saved.get(username, DEFAULT_STATUS)
            name_col, status_col = st.columns([3, 2])
            name_col.markdown(f"**{full_name}**  \n{grade}")
            # The saved status is part of the key, so the radio resets
            # whenever the database value changes (e.g. after saving).
            selections[username] = status_col.radio(
                full_name,
                STATUS_OPTIONS,
                index=STATUS_OPTIONS.index(default),
                key=f"roll_{attendance_date}_{username}_{saved.get(username, 'new')}",
                horizontal=True,
                label_visibility="collapsed",
            )
        submitted = st.form_submit_button("Save attendance", type="primary")

    if submitted:
        try:
            count = save_bulk_attendance(attendance_date, selections)
            present = list(selections.values()).count("Present")
            st.success(
                f"Saved {count} records for {attendance_date}: "
                f"{present} present, {count - present} absent."
            )
        except DatabaseConnectionError as e:
            st.error(str(e))
        except psycopg.Error as e:
            st.error(f"Database error: {e}")