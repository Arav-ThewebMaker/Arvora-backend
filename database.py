import os
import psycopg


DATABASE_URL = os.getenv("DATABASE_URL")


def connect():
    return psycopg.connect(DATABASE_URL)
