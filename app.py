import os
import sqlite3
import requests
from dotenv import load_dotenv

# 1. Setup & Credentials
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")
DB_NAME = "cineflow.db"

def save_to_db(movie_data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO movies (tmdb_id, title, release_date, overview)
            VALUES (?, ?, ?, ?)
        ''', (movie_data['id'], movie_data['title'], 
              movie_data.get('release_date'), movie_data.get('overview')))
        
        conn.commit()
        print(f"✅ Saved '{movie_data['title']}' to your collection!")
    except sqlite3.IntegrityError:
        print(f"ℹ️ '{movie_data['title']}' is already in your collection.")
    finally:
        conn.close()

def fetch_and_collect(movie_name):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {"api_key": API_KEY, "query": movie_name}
    
    response = requests.get(url, params=params)
    
    # DEBUG LINE: Let's see the status and the raw data
    print(f"DEBUG: Status Code: {response.status_code}")
    
    data = response.json()
    results = data.get('results')

    if results:
        top_movie = results[0]
        save_to_db(top_movie)
    else:
        # DEBUG LINE: See what the actual JSON looks like if results are empty
        print(f"DEBUG: Full JSON Response: {data}")
        print("❌ No movie found with that name.")

if __name__ == "__main__":
    search = input("What movie would you like to add to your collection? ")
    fetch_and_collect(search)