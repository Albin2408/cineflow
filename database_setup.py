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
            poster_path TEXT,
            watch_count INTEGER DEFAULT 0,
            added_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create the ratings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_id INTEGER NOT NULL,
            rating REAL CHECK(rating >= 0 AND rating <= 10),
            review TEXT,
            mood TEXT,
            rated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (movie_id) REFERENCES movies(id)
        )
    ''')

    # Create the watchlist table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS watchlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tmdb_id INTEGER UNIQUE,
            title TEXT NOT NULL,
            release_date TEXT,
            overview TEXT,
            poster_path TEXT,
            added_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized with all tables: movies, ratings, and watchlist!")

if __name__ == "__main__":
    init_db()