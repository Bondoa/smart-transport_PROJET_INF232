import sqlite3

def get_connection():
    conn = sqlite3.connect("transport.db")
    return conn


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transport (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT,
        depart TEXT,
        arrivee TEXT,
        moyen TEXT,
        temps REAL,
        cout REAL,
        satisfaction INTEGER
    )
    """)

    conn.commit()
    conn.close()
