from database import connect

conn = connect()
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users(
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS subjects(
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    name TEXT UNIQUE,
    priority INTEGER
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS exams(
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    subject TEXT NOT NULL,
    date DATE NOT NULL,
    target_percentage INTEGER CHECK(target_percentage BETWEEN 0 AND 100),
    current_percentage INTEGER CHECK(current_percentage BETWEEN 0 AND 100),
    importance INTEGER CHECK(importance BETWEEN 1 AND 5),
    UNIQUE(subject, date)
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS study_sessions(
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    subject TEXT NOT NULL,
    chapter_name TEXT,
    date DATE NOT NULL,
    minutes INTEGER CHECK(minutes >= 0),
    focus INTEGER CHECK(focus BETWEEN 1 AND 10),
    method TEXT,
    rating INTEGER CHECK(rating BETWEEN 1 AND 10)
)
""")

conn.commit()
cur.close()
conn.close()

print("PostgreSQL tables created successfully!")
