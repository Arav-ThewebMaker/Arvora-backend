from psycopg_pool import ConnectionPool
import os


pool = ConnectionPool(
    conninfo=os.getenv("DATABASE_URL"),
    min_size=1,
    max_size=10,
    max_idle=30,
    timeout=10,
    reconnect_timeout=5
)
