import sqlite3

def init_db():
    # Connect to the database file (it will be created if it doesn't exist)
    conn = sqlite3.connect('cineflow.db')
    cursor = conn.cursor()

    # Create the movies table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tmdb_id INTEGER UNIQUE,
            title TEXT NOT NULL,
            release_date TEXT,
            overview TEXT,
            added_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized and 'movies' table is ready!")

if __name__ == "__main__":
    init_db()