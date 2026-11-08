
"""Payments tab: record a payment and see who has paid for a month."""
import calendar
from datetime import date

import pandas as pd
import psycopg
import streamlit as st

from src.attendance_service import DatabaseConnectionError, get_active_students
from src.payment_service import PaymentError, get_month_overview, record_payment


PAYMENT_METHODS = ["Cash", "Bank Transfer", "Wallet"]
RECEIVERS = ["Youssef", "Mama"]
PAYMENT_TIMINGS = ["Prepaid", "Postpaid"]
MONTH_NAMES = list(calendar.month_name)[1:]


def _flash(kind, text):
    """Keep a message across the st.rerun() that refreshes the overview."""
    st.session_state["payments_flash"] = (kind, text)


def render_payments():
    st.subheader("Payments")
    today = date.today()

    flash = st.session_state.pop("payments_flash", None)
    if flash:
        kind, text = flash
        getattr(st, kind)(text)

    # Month and year selection
    col_month, col_year = st.columns(2)

    month_name = col_month.selectbox(
        "Month",
        MONTH_NAMES,
        index=today.month - 1,
        key="pay_month",
    )

    years = list(range(today.year - 2, today.year + 2))
    year = col_year.selectbox(
        "Year",
        years,
        index=years.index(today.year),
        key="pay_year",
    )

    period_month = date(year, MONTH_NAMES.index(month_name) + 1, 1)
    period_label = f"{month_name} {year}"

    # ------------------------------------------------------------- Form
    st.markdown(f"#### Record a payment for {period_label}")

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
        labels = {u: f"{n} ({g})" for u, n, g in students}

        # Refresh form widgets after successful submission
        n = st.session_state.setdefault("pay_form_n", 0)

        with st.form(f"payment_form_{n}"):

            username = st.selectbox(
                "Student",
                options=list(labels),
                format_func=lambda u: labels[u],
                key=f"pay_student_{n}",
            )

            amount = st.number_input(
                "Amount",
                min_value=1,
                step=1,
                value=None,
                key=f"pay_amount_{n}",
            )

            payment_date = st.date_input(
                "Payment date",
                value=today,
                key=f"pay_date_{n}",
            )

            method = st.selectbox(
                "Payment method",
                PAYMENT_METHODS,
                key=f"pay_method_{n}",
            )

            payment_timing = st.selectbox(
                "Payment timing",
                PAYMENT_TIMINGS,
                index=None,
                placeholder="Prepaid or Postpaid",
                key=f"pay_timing_{n}",
            )

            received_by = st.selectbox(
                "Received by",
                RECEIVERS,
                key=f"pay_receiver_{n}",
            )

            notes = st.text_input(
                "Notes (optional)",
                key=f"pay_notes_{n}",
            )

            submitted = st.form_submit_button(
                "Record payment",
                type="primary",
            )

        if submitted:

            if amount is None:
                st.error("Enter the amount.")

            elif payment_timing is None:
                st.error("Choose Prepaid or Postpaid.")

            else:
                try:
                    payment_id = record_payment(
                        username,
                        amount,
                        payment_date,
                        method,
                        period_month,
                        received_by,
                        payment_timing,
                        notes,
                    )

                    st.session_state["pay_form_n"] = n + 1

                    _flash(
                        "success",
                        f"Payment #{payment_id} recorded: {amount} from "
                        f"{labels[username]} for {period_label}.",
                    )

                    st.rerun()

                except PaymentError as e:
                    st.error(str(e))

    st.divider()

    # --------------------------------------------------------- Overview
    st.markdown(f"#### Who has paid for {period_label}")

    try:
        rows = get_month_overview(period_month)

    except PaymentError as e:
        st.error(str(e))
        return

    if not rows:
        st.info("No students to show.")
        return

    df = pd.DataFrame(
        rows,
        columns=[
            "Username",
            "Name",
            "Grade",
            "Payment exempt",
            "Total paid",
            "Last payment",
            "Timing",
        ],
    )

    # Determine payment status
    df["Status"] = "Exempt"

    df.loc[
        ~df["Payment exempt"] & (df["Total paid"] > 0),
        "Status",
    ] = "Paid"

    df.loc[
        ~df["Payment exempt"] & (df["Total paid"] <= 0),
        "Status",
    ] = "Not paid"

    # Count only students who are required to pay
    eligible_count = int((~df["Payment exempt"]).sum())

    paid_count = int(
        (
            (~df["Payment exempt"])
            & (df["Total paid"] > 0)
        ).sum()
    )

    st.caption(
        f"{paid_count} of {eligible_count} students have paid for "
        f"{period_label}. "
        f"Total received: {int(df['Total paid'].sum())}. "
        "Most recent payments first."
    )

    st.dataframe(
        df[
            [
                "Name",
                "Grade",
                "Status",
                "Total paid",
                "Last payment",
                "Timing",
            ]
        ],
        width="stretch",
        hide_index=True,
    )
