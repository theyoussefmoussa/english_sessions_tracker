import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    try:
        conn = psycopg.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
        )
        return conn

    except psycopg.Error as error:
        print(f"Connection failed: {error}")
        return None