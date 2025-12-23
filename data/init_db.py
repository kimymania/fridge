from pathlib import Path
from sqlite3 import Connection, Cursor, connect


def create_db() -> tuple[Connection, Cursor]:
    top_dir = Path(__file__).resolve().parents[1]
    db_dir = top_dir / "db"
    db_dir.mkdir(exist_ok=True)
    db_name = "ubion.db"
    db_path = str(db_dir / db_name)

    conn = connect(db_path, check_same_thread=False)
    curs = conn.cursor()
    return conn, curs


conn, curs = create_db()


def init_db():
    conn, curs = create_db()
    curs.execute("""
        CREATE TABLE IF NOT EXISTS user(
        name TEXT PRIMARY KEY,
        email TEXT,
        hashed_password TEXT)
    """)
    curs.execute("""CREATE TABLE IF NOT EXISTS refrigerator(
        food_name TEXT PRIMARY KEY,
        quantity INTEGER,
        user TEXT,
        FOREIGN KEY (user) REFERENCES user(name)
        ON DELETE CASCADE
    )""")
    conn.commit()
    conn.close()
