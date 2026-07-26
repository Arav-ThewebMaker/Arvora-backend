from psycopg_pool import ConnectionPool
import os

pool = ConnectionPool(
    conninfo=os.getenv("DATABASE_URL"),
    min_size=2,
    max_size=10,
    timeout=30,
    max_idle=300,
    check=ConnectionPool.check_connection
)
