import streamlit as st
import sqlite3
import pandas as pd
import requests
import os
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Page configuration
st.set_page_config(page_title="CineFlow AI", page_icon="🎬")
st.title("🎬 CineFlow: AI Movie Discovery")

# Load environment
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# --- Helper Functions ---
def get_data():
    conn = sqlite3.connect('cineflow.db')
    df = pd.read_sql_query("SELECT * FROM movies", conn)
    conn.close()
    return df

def search_tmdb(query):
    """Search TMDB for movies matching the query"""
    if not query or len(query) < 2:
        return []
    
    url = "https://api.themoviedb.org/3/search/movie"
    params = {"api_key": TMDB_API_KEY, "query": query}
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        results = data.get('results', [])
        return results[:10]  # Return top 10 results
    except:
        return []

def save_to_db(movie_data):
    """Save movie to database"""
    conn = sqlite3.connect('cineflow.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO movies (tmdb_id, title, release_date, overview, poster_path)
            VALUES (?, ?, ?, ?, ?)
        ''', (movie_data['id'], movie_data['title'], 
              movie_data.get('release_date'), movie_data.get('overview'),
              movie_data.get('poster_path')))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def save_rating(movie_id, rating, review):
    """Save or update a rating and review"""
    conn = sqlite3.connect('cineflow.db')
    cursor = conn.cursor()
    
    try:
        # Check if rating already exists
        cursor.execute('SELECT id FROM ratings WHERE movie_id = ?', (movie_id,))
        existing = cursor.fetchone()
        
        if existing:
            cursor.execute('UPDATE ratings SET rating = ?, review = ? WHERE movie_id = ?',
                         (rating, review, movie_id))
        else:
            cursor.execute('INSERT INTO ratings (movie_id, rating, review) VALUES (?, ?, ?)',
                         (movie_id, rating, review))
        conn.commit()
        return True
    except Exception as e:
        return False
    finally:
        conn.close()

def get_rating(movie_id):
    """Get rating and review for a movie"""
    conn = sqlite3.connect('cineflow.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT rating, review FROM ratings WHERE movie_id = ?', (movie_id,))
        result = cursor.fetchone()
        return result if result else (0, "")
    except:
        return (0, "")
    finally:
        conn.close()

def add_to_watchlist(movie_data):
    """Add movie to watchlist"""
    conn = sqlite3.connect('cineflow.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO watchlist (tmdb_id, title, release_date, overview, poster_path)
            VALUES (?, ?, ?, ?, ?)
        ''', (movie_data['id'], movie_data['title'], 
              movie_data.get('release_date'), movie_data.get('overview'),
              movie_data.get('poster_path')))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def remove_from_watchlist(tmdb_id):
    """Remove movie from watchlist"""
    conn = sqlite3.connect('cineflow.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('DELETE FROM watchlist WHERE tmdb_id = ?', (tmdb_id,))
        conn.commit()
    except:
        pass
    finally:
        conn.close()

def get_watchlist():
    """Get all movies in watchlist"""
    conn = sqlite3.connect('cineflow.db')
    df = pd.read_sql_query("SELECT * FROM watchlist ORDER BY added_at DESC", conn)
    conn.close()
    return df

def save_rating_with_mood(movie_id, rating, review, mood):
    """Save or update a rating, review, and mood"""
    conn = sqlite3.connect('cineflow.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT id FROM ratings WHERE movie_id = ?', (movie_id,))
        existing = cursor.fetchone()
        
        if existing:
            cursor.execute('UPDATE ratings SET rating = ?, review = ?, mood = ? WHERE movie_id = ?',
                         (rating, review, mood, movie_id))
        else:
            cursor.execute('INSERT INTO ratings (movie_id, rating, review, mood) VALUES (?, ?, ?, ?)',
                         (movie_id, rating, review, mood))
        conn.commit()
        return True
    except Exception as e:
        return False
    finally:
        conn.close()

def get_rating_with_mood(movie_id):
    """Get rating, review, and mood for a movie"""
    conn = sqlite3.connect('cineflow.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT rating, review, mood FROM ratings WHERE movie_id = ?', (movie_id,))
        result = cursor.fetchone()
        return result if result else (0, "", None)
    except:
        return (0, "", None)
    finally:
        conn.close()

def search_by_mood(mood):
    """Search TMDB for movies based on mood/keywords"""
    mood_keywords = {
        "Happy": "comedy funny",
        "Sad": "drama emotional",
        "Scary": "horror thriller",
        "Action": "action adventure",
        "Romantic": "romance love",
        "Inspiring": "inspirational motivation",
        "Adventurous": "adventure fantasy",
        "Mysterious": "mystery suspense"
    }
    
    query = mood_keywords.get(mood, mood)
    url = "https://api.themoviedb.org/3/search/movie"
    params = {"api_key": TMDB_API_KEY, "query": query}
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        results = data.get('results', [])
        return results[:10]
    except:
        return []

def get_yearly_stats():
    """Get statistics for yearly wrap-up"""
    conn = sqlite3.connect('cineflow.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT COUNT(*) as total_movies, 
                   AVG(rating) as avg_rating,
                   MAX(rating) as highest_rating,
                   strftime('%Y', rated_at) as year
            FROM ratings
            WHERE strftime('%Y', rated_at) = strftime('%Y', 'now')
            GROUP BY year
        ''')
        result = cursor.fetchone()
        return result if result else (0, 0, 0, 0)
    except:
        return (0, 0, 0, 0)
    finally:
        conn.close()

def get_monthly_stats():
    """Get statistics for monthly wrap-up"""
    conn = sqlite3.connect('cineflow.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT COUNT(*) as total_movies,
                   AVG(rating) as avg_rating,
                   strftime('%Y-%m', rated_at) as month
            FROM ratings
            WHERE strftime('%Y-%m', rated_at) = strftime('%Y-%m', 'now')
        ''')
        result = cursor.fetchone()
        return result if result else (0, 0, None)
    except:
        return (0, 0, None)
    finally:
        conn.close()

def increment_watch_count(movie_id):
    """Increment the watch count for a movie"""
    conn = sqlite3.connect('cineflow.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('UPDATE movies SET watch_count = watch_count + 1 WHERE id = ?', (movie_id,))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def get_watch_count(movie_id):
    """Get watch count for a movie"""
    conn = sqlite3.connect('cineflow.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT watch_count FROM movies WHERE id = ?', (movie_id,))
        result = cursor.fetchone()
        return result[0] if result else 0
    except:
        return 0
    finally:
        conn.close()

def get_top_rewatched_movies(limit=5):
    """Get top rewatched movies"""
    conn = sqlite3.connect('cineflow.db')
    df = pd.read_sql_query(
        f"SELECT title, watch_count FROM movies WHERE watch_count > 0 ORDER BY watch_count DESC LIMIT {limit}",
        conn
    )
    conn.close()
    return df

def get_total_rewatch_count():
    """Get total rewatch count"""
    conn = sqlite3.connect('cineflow.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT SUM(watch_count) FROM movies')
        result = cursor.fetchone()
        return result[0] if result and result[0] else 0
    except:
        return 0
    finally:
        conn.close()



def get_recommendations(tmdb_id):
    """Get recommendations from TMDB for a specific movie"""
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/recommendations"
    params = {"api_key": TMDB_API_KEY}
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        results = data.get('results', [])
        return results
    except:
        return []

# --- Sidebar: Your Collection & Watchlist ---
st.sidebar.header("📚 Your Library")
collection_tab, watchlist_tab = st.sidebar.tabs(["Collection", "Watchlist"])

df = get_data()
watchlist_df = get_watchlist()

with collection_tab:
    if not df.empty:
        display_df = df[['title', 'release_date', 'watch_count']].copy()
        display_df.columns = ['Title', 'Year', 'Rewatches']
        st.dataframe(display_df, hide_index=True, use_container_width=True)
    else:
        st.write("Your collection is empty.")

with watchlist_tab:
    if not watchlist_df.empty:
        st.dataframe(watchlist_df[['title', 'release_date']], hide_index=True, use_container_width=True)
    else:
        st.write("Your watchlist is empty.")

# --- Main UI: Search and Add ---
st.subheader("Add a New Movie")

# Search input with autocomplete
search_query = st.text_input("Search TMDB for a movie to add:", key="search_input")

# Get suggestions from TMDB
suggestions = []
if search_query:
    results = search_tmdb(search_query)
    suggestions = [f"{movie['title']} ({movie.get('release_date', 'N/A')[:4]})" for movie in results]

# Display suggestions and let user select
if suggestions:
    selected = st.selectbox(
        "Select a movie from suggestions:",
        suggestions,
        key="movie_select"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Add to Collection"):
            # Find the selected movie in the results
            results = search_tmdb(search_query)
            for movie in results:
                movie_display = f"{movie['title']} ({movie.get('release_date', 'N/A')[:4]})"
                if movie_display == selected:
                    added = save_to_db(movie)
                    if added:
                        st.success(f"✅ Added '{movie['title']}' to your collection!")
                    else:
                        st.info(f"ℹ️ '{movie['title']}' is already in your collection.")
                    st.rerun()
                    break
    
    with col2:
        if st.button("📌 Add to Watchlist"):
            # Find the selected movie in the results
            results = search_tmdb(search_query)
            for movie in results:
                movie_display = f"{movie['title']} ({movie.get('release_date', 'N/A')[:4]})"
                if movie_display == selected:
                    added = add_to_watchlist(movie)
                    if added:
                        st.success(f"📌 Added '{movie['title']}' to your watchlist!")
                    else:
                        st.info(f"ℹ️ '{movie['title']}' is already in your watchlist.")
                    st.rerun()
                    break
else:
    if search_query:
        st.info("No movies found. Try a different search!")

# --- Main UI: Recommendations ---
st.divider()
st.subheader("AI Recommendations")

if len(df) >= 1:
    selected_movie = st.selectbox("Pick a movie you liked:", df['title'].values)
    
    # Get the TMDB ID of the selected movie
    selected_row = df[df['title'] == selected_movie]
    if not selected_row.empty:
        tmdb_id = int(selected_row.iloc[0]['tmdb_id'])
        
        # Get recommendations from TMDB
        recommendations = get_recommendations(tmdb_id)
        
        # Get list of movies already watched (to filter them out)
        watched_titles = set(df['title'].values)
        
        # Filter recommendations to only include movies not watched
        new_recommendations = [
            movie for movie in recommendations 
            if movie.get('title') not in watched_titles
        ]
        
        if new_recommendations:
            st.write(f"Because you liked **{selected_movie}**, you might enjoy:")
            
            # Display recommendations in columns
            cols = st.columns(5)  # Display 5 movies across
            for idx, movie in enumerate(new_recommendations[:5]):
                with cols[idx % 5]:
                    poster_path = movie.get('poster_path')
                    if poster_path:
                        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                        st.image(poster_url, caption=f"{movie['title']} ({movie.get('release_date', 'N/A')[:4]})")
                    else:
                        st.info(f"🎥 {movie['title']} ({movie.get('release_date', 'N/A')[:4]})")
                    
                    # Show rating and overview
                    rating = movie.get('vote_average', 0)
                    st.caption(f"⭐ {rating}/10")
        else:
            st.info("No new recommendations available. You might have seen them all!")
else:
    st.warning("Add at least 1 movie to enable AI recommendations.")

# --- Main UI: Rate & Review ---
st.divider()
st.subheader("⭐ Rate & Review Your Movies")

if len(df) >= 1:
    movie_to_rate = st.selectbox("Select a movie to rate:", df['title'].values, key="rate_select")
    
    movie_row = df[df['title'] == movie_to_rate]
    if not movie_row.empty:
        movie_id = int(movie_row.iloc[0]['id'])
        current_rating, current_review, current_mood = get_rating_with_mood(movie_id)
        
        # Rating slider (0-10 with decimals)
        rating = st.slider("Your rating (0-10):", 0.0, 10.0, value=float(current_rating) if current_rating > 0 else 5.0, step=0.1, key="rating_slider")
        
        # Mood selection
        moods = ["😊 Happy", "😢 Sad", "😨 Scary", "💪 Action", "❤️ Romantic", "✨ Inspiring", "🗺️ Adventurous", "🔍 Mysterious"]
        mood_value = st.selectbox("How did this movie make you feel?", moods, index=0, key="mood_select")
        mood = mood_value.split(" ")[1]
        
        # Review text
        review = st.text_area("Your review:", value=current_review, key="review_text", placeholder="What did you think about this movie?")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save Rating & Review"):
                if save_rating_with_mood(movie_id, rating, review, mood):
                    st.success(f"✅ Rating saved! You gave '{movie_to_rate}' {rating}/10⭐ (Mood: {mood})")
                else:
                    st.error("Failed to save rating.")
        
        with col2:
            watch_count = get_watch_count(movie_id)
            if st.button("🔄 I Watched This Again"):
                if increment_watch_count(movie_id):
                    st.success(f"✅ Rewatch logged! You've watched '{movie_to_rate}' {watch_count + 1} times")
                    st.rerun()
                else:
                    st.error("Failed to log rewatch.")
        
        # Show current watch count
        current_watch_count = get_watch_count(movie_id)
        if current_watch_count > 0:
            st.info(f"📺 You've watched this **{current_watch_count}** {"time" if current_watch_count == 1 else "times"}")
else:
    st.info("Add movies to your collection to rate them!")

# --- Main UI: Mood-Based Search ---
st.divider()
st.subheader("🎯 Search by Mood")

moods_for_search = ["😊 Happy", "😢 Sad", "😨 Scary", "💪 Action", "❤️ Romantic", "✨ Inspiring", "🗺️ Adventurous", "🔍 Mysterious"]
selected_mood = st.selectbox("Choose a mood to discover movies:", moods_for_search, key="mood_search")
mood_query = selected_mood.split(" ")[1]

if st.button("🔍 Find movies by mood"):
    mood_results = search_by_mood(mood_query)
    if mood_results:
        st.write(f"Movies for when you're feeling {mood_query}:")
        cols = st.columns(5)
        for idx, movie in enumerate(mood_results[:5]):
            with cols[idx % 5]:
                poster_path = movie.get('poster_path')
                if poster_path:
                    poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                    st.image(poster_url, caption=f"{movie['title']} ({movie.get('release_date', 'N/A')[:4]})")
                else:
                    st.info(f"🎥 {movie['title']}")
                
                if st.button(f"Add to Collection", key=f"add_mood_{movie['id']}"):
                    if save_to_db(movie):
                        st.success(f"✅ Added to collection!")
                    else:
                        st.info("Already in collection")
    else:
        st.info("No movies found for this mood")

# --- Main UI: Wrap-Ups ---
st.divider()
st.subheader("📊 Your Stats & Wrap-Ups")

wrap_tab1, wrap_tab2 = st.tabs(["This Month", "This Year"])

with wrap_tab1:
    st.write("**📅 This Month's Stats**")
    monthly_stats = get_monthly_stats()
    if monthly_stats[0] > 0:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Movies Watched", int(monthly_stats[0]))
        with col2:
            st.metric("Average Rating", f"{monthly_stats[1]:.1f}/10")
        with col3:
            conn = sqlite3.connect('cineflow.db')
            cursor = conn.cursor()
            cursor.execute('''
                SELECT mood, COUNT(*) as count FROM ratings
                WHERE strftime('%Y-%m', rated_at) = strftime('%Y-%m', 'now')
                GROUP BY mood ORDER BY count DESC LIMIT 1
            ''')
            top_mood = cursor.fetchone()
            conn.close()
            mood_display = top_mood[0] if top_mood else "N/A"
            st.metric("Top Mood", mood_display)
        
        # Show total rewatches this month
        st.divider()
        total_rewatches = get_total_rewatch_count()
        if total_rewatches > 0:
            st.metric("Total Rewatches (Overall)", total_rewatches)
            
            # Show top 5 rewatched movies
            st.subheader("🎬 Your Top Rewatched Movies")
            top_movies = get_top_rewatched_movies(5)
            if not top_movies.empty:
                for idx, row in top_movies.iterrows():
                    st.write(f"**{idx + 1}. {row['title']}** - Watched {int(row['watch_count'])} times")
    else:
        st.info("No movies rated this month yet!")

with wrap_tab2:
    st.write("**🎬 This Year's Wrap-Up**")
    yearly_stats = get_yearly_stats()
    if yearly_stats[0] > 0:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Movies Watched", int(yearly_stats[0]))
        with col2:
            st.metric("Average Rating", f"{yearly_stats[1]:.1f}/10")
        with col3:
            st.metric("Highest Rating", f"{yearly_stats[2]:.1f}/10")
        
        # Show total rewatches
        st.divider()
        total_rewatches = get_total_rewatch_count()
        st.metric("Total Rewatches (Overall)", total_rewatches)
        
        # Show top 5 rewatched movies
        st.subheader("🏆 Your Top 5 Most Rewatched Movies")
        top_movies = get_top_rewatched_movies(5)
        if not top_movies.empty:
            for idx, row in top_movies.iterrows():
                st.write(f"**{idx + 1}. {row['title']}** - Watched {int(row['watch_count'])} times")
        
        # Download button for stats
        top_movies_text = "\n".join([f"{idx + 1}. {row['title']} - Watched {int(row['watch_count'])} times" for idx, row in top_movies.iterrows()]) if not top_movies.empty else "No rewatches yet"
        
        stats_text = f"""CineFlow Yearly Wrap-Up {yearly_stats[3]}
        
Total Movies Rated: {int(yearly_stats[0])}
Average Rating: {yearly_stats[1]:.1f}/10
Highest Rating: {yearly_stats[2]:.1f}/10

Total Rewatches: {total_rewatches}

Top 5 Most Rewatched Movies:
{top_movies_text}

Thanks for using CineFlow! 🎬
"""
        st.download_button(
            label="📥 Download Wrap-Up",
            data=stats_text,
            file_name=f"cineflow_wrap_up_{yearly_stats[3]}.txt",
            mime="text/plain"
        )
    else:
        st.info("No movies rated this year yet!")