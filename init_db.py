from database import connect

conn = connect()
cur = conn.cursor()

# Create users table
cur.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL
)
""")

# Create subjects table
cur.execute("""
CREATE TABLE IF NOT EXISTS subjects(
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    name TEXT UNIQUE,
    priority INTEGER
)
""")

# Create exams table
cur.execute("""
CREATE TABLE IF NOT EXISTS exams (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    subject TEXT NOT NULL,
    date TEXT NOT NULL,
    target_percentage INTEGER
        CHECK(target_percentage BETWEEN 0 AND 100),
    current_percentage INTEGER
        CHECK(current_percentage BETWEEN 0 AND 100),
    importance INTEGER
        CHECK(importance BETWEEN 1 AND 5),
    UNIQUE(subject, date)
)
""")

# Create study sessions table
cur.execute("""
CREATE TABLE IF NOT EXISTS study_sessions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    subject TEXT NOT NULL,
    chapter_name TEXT,
    date TEXT NOT NULL,
    minutes INTEGER
        CHECK(minutes >= 0),
    focus INTEGER
        CHECK(focus BETWEEN 1 AND 10),
    method TEXT,
    rating INTEGER
        CHECK(rating BETWEEN 1 AND 10)
)
""")

conn.commit()
conn.close()

print("Data Tables created succesfully!")
