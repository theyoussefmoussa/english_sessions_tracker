import os
from datetime import date

import pandas as pd
import psycopg
import streamlit as st

try:
    if "DATABASE_URL" in st.secrets:
        os.environ["DATABASE_URL"] = st.secrets["DATABASE_URL"]
except FileNotFoundError:
    pass

from src.attendance_service import (
    DatabaseConnectionError,
    get_active_students,
    get_all_attendance,
    get_attendance_status,
    insert_attendance,
    update_attendance,
)
st.set_page_config(page_title="Student Attendance Tracker", page_icon="📋")
st.title("Student Attendance Tracker")

# Holds a record waiting for the user to confirm an overwrite
if "pending_overwrite" not in st.session_state:
    st.session_state.pending_overwrite = None

mark_tab, view_tab = st.tabs(["Mark Attendance", "View Attendance"])


# ---------------------------------------------------------------- Mark tab
with mark_tab:
    st.subheader("Mark attendance")

    try:
        students = get_active_students()
    except DatabaseConnectionError as e:
        st.error(str(e))
        students = []
    except psycopg.Error as e:
        st.error(f"Database error: {e}")
        students = []

    if not students:
        st.info("No active students found.")
    else:
        # students = [(username, full_name, grade), ...]
        usernames = [s[0] for s in students]
        labels = {s[0]: f"{s[1]} ({s[2]})" for s in students}

        with st.form("mark_attendance_form"):
            username = st.selectbox(
                "Student", options=usernames, format_func=lambda u: labels[u]
            )
            attendance_date = st.date_input("Date", value=date.today())
            status = st.radio("Status", ["Present", "Absent"], horizontal=True)
            submitted = st.form_submit_button("Record attendance")

        if submitted:
            st.session_state.pending_overwrite = None  # reset any old prompt
            try:
                existing = get_attendance_status(username, attendance_date)

                if existing is None:
                    insert_attendance(username, attendance_date, status)
                    st.success(
                        f"Attendance for {labels[username]} on {attendance_date} "
                        f"has been recorded as {status}."
                    )
                elif existing == status:
                    st.info(
                        f"{labels[username]} is already marked {existing} "
                        f"on {attendance_date}. Nothing to change."
                    )
                else:
                    st.session_state.pending_overwrite = {
                        "username": username,
                        "label": labels[username],
                        "date": attendance_date,
                        "old_status": existing,
                        "new_status": status,
                    }
            except DatabaseConnectionError as e:
                st.error(str(e))
            except psycopg.Error as e:
                st.error(f"Database error: {e}")

        # Overwrite confirmation (lives outside the form so buttons work)
        pending = st.session_state.pending_overwrite
        if pending:
            st.warning(
                f"Attendance for {pending['label']} on {pending['date']} is already "
                f"recorded as **{pending['old_status']}**. "
                f"Overwrite it with **{pending['new_status']}**?"
            )
            col_yes, col_no, _ = st.columns([1, 1, 3])

            if col_yes.button("Overwrite", type="primary"):
                try:
                    update_attendance(
                        pending["username"], pending["date"], pending["new_status"]
                    )
                    st.session_state.pending_overwrite = None
                    st.success(
                        f"Updated {pending['label']} on {pending['date']} "
                        f"to {pending['new_status']}."
                    )
                except DatabaseConnectionError as e:
                    st.error(str(e))
                except psycopg.Error as e:
                    st.error(f"Database error: {e}")

            if col_no.button("Cancel"):
                st.session_state.pending_overwrite = None
                st.rerun()


# ---------------------------------------------------------------- View tab
with view_tab:
    st.subheader("All attendance records")

    try:
        columns, rows = get_all_attendance()
        if not rows:
            st.info("No attendance records found.")
        else:
            st.dataframe(
                pd.DataFrame(rows, columns=columns),
                use_container_width=True,
                hide_index=True,
            )
    except DatabaseConnectionError as e:
        st.error(str(e))
    except psycopg.Error as e:
        st.error(f"Database error: {e}")