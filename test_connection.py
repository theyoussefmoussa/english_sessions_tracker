
import os

import psycopg
from dotenv import load_dotenv # type: ignore

load_dotenv()

try:
    with psycopg.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT current_database(), current_user;"
            )
            database, user = cur.fetchone()

            print("Connection successful!")
            print(f"Database: {database}")
            print(f"User: {user}")

except psycopg.Error as error:
    print(f"Connection failed: {error}")
