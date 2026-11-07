import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    try:
        database_url = os.getenv("DATABASE_URL")

        if database_url:
            return psycopg.connect(database_url)

        return psycopg.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
        )

    except psycopg.Error as error:
        print(f"Connection failed: {error}")
        return None