
"""Database functions for payments (no input() / print(); the UI shows results)."""
import psycopg

from database.connection import get_connection


class PaymentError(Exception):
    """Raised when a payment-related error occurs."""


# Friendly messages for the CHECK constraints on the payment table
_CONSTRAINT_MESSAGES = {
    "payment_amount_check": "Amount must be greater than 0.",
    "payment_payment_method_check": "Payment method must be Cash, Bank Transfer or Wallet.",
    "payment_payment_timing_check": "Payment timing must be Prepaid or Postpaid.",
    "payment_received_by_check": "Received by must be Youssef or Mama.",
    "payment_period_month_check": "Period month must be the first day of a month.",
}


def _connect():
    conn = get_connection()
    if conn is None:
        raise PaymentError("Unable to connect to the database.")
    return conn


def record_payment(username, amount, payment_date, payment_method,
                   period_month, received_by, payment_timing, notes=None):
    """Insert one payment and return its payment_id.

    period_month is normalised to the first day of its month.
    payment_timing is 'Prepaid' or 'Postpaid'.
    """
    period_month = period_month.replace(day=1)
    notes = (notes or "").strip() or None

    conn = _connect()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO payment
                        (username, date, period_month, amount,
                         payment_method, payment_timing, received_by, notes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING payment_id;
                """, (
                    username, payment_date, period_month, amount,
                    payment_method, payment_timing, received_by, notes
                ))
                return cur.fetchone()[0]

    except psycopg.errors.ForeignKeyViolation as e:
        raise PaymentError(f"Student '{username}' does not exist.") from e

    except psycopg.errors.CheckViolation as e:
        message = _CONSTRAINT_MESSAGES.get(
            e.diag.constraint_name, "Payment details are invalid."
        )
        raise PaymentError(message) from e

    except psycopg.errors.NotNullViolation as e:
        raise PaymentError("A required payment field is missing.") from e

    except psycopg.Error as e:
        raise PaymentError(f"Failed to record payment: {e}") from e

    finally:
        conn.close()


def get_month_overview(period_month):
    """Return payment overview for the selected month.

    Each row:
    (username, full_name, grade, payment_exempt,
     total_paid, last_payment_date, timing).

    Includes every active student, plus deactivated students
    who paid for that month.
    """
    period_month = period_month.replace(day=1)

    conn = _connect()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT s.username,
                           s.full_name,
                           s.grade::text,
                           s.payment_exempt,
                           COALESCE(SUM(p.amount), 0) AS total_paid,
                           MAX(p.date) AS last_payment_date,
                           STRING_AGG(DISTINCT p.payment_timing, ', ') AS timing
                    FROM students s
                    LEFT JOIN payment p
                           ON p.username = s.username
                          AND p.period_month = %s
                    WHERE s.is_active = TRUE OR p.payment_id IS NOT NULL
                    GROUP BY s.username, s.full_name, s.grade,
                             s.payment_exempt
                    ORDER BY MAX(p.date) DESC NULLS LAST, s.full_name;
                """, (period_month,))
                return cur.fetchall()

    except psycopg.Error as e:
        raise PaymentError(f"Failed to load payments: {e}") from e

    finally:
        conn.close()
