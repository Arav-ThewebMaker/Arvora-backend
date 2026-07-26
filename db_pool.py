from psycopg_pool import ConnectionPool

pool = ConnectionPool(
    conninfo="postgresql://neondb_owner:npg_MsfDYWV8mQ1q@ep-jolly-mountain-azabl7q8-pooler.c-3.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require",
    min_size=1,
    max_size=10
)
