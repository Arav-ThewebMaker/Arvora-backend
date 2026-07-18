import sqlite3


def connect():
    conn = sqlite3.connect("data/arvora.db", timeout=10)
    return conn
