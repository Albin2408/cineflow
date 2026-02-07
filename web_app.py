import streamlit as st
import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Page configuration
st.set_page_config(page_title="CineFlow AI", page_icon="🎬")
st.title("🎬 CineFlow: AI Movie Discovery")

# --- Helper Functions ---
def get_data():
    conn = sqlite3.connect('cineflow.db')
    df = pd.read_sql_query("SELECT * FROM movies", conn)
    conn.close()
    return df

# --- Sidebar: Your Collection ---
st.sidebar.header("Your Collection")
df = get_data()
if not df.empty:
    st.sidebar.dataframe(df[['title', 'release_date']], hide_index=True)
else:
    st.sidebar.write("Your library is empty.")

# --- Main UI: Search and Add ---
st.subheader("Add a New Movie")
movie_name = st.text_input("Search TMDB for a movie to add:")

if st.button("Search & Add"):
    # This calls the logic from your app.py
    import subprocess
    # We pass the input to your existing script
    process = subprocess.Popen(['python3', 'app.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate(input=movie_name)
    st.success(f"Processed: {movie_name}")
    st.rerun()

# --- Main UI: Recommendations ---
st.divider()
st.subheader("AI Recommendations")

if len(df) >= 2:
    selected_movie = st.selectbox("Pick a movie you liked:", df['title'].values)
    
    # ML Logic
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['overview'].fillna(''))
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    idx = df[df['title'] == selected_movie].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    st.write(f"Because you liked **{selected_movie}**, you might enjoy:")
    for i, score in sim_scores[1:3]:
        match = df.iloc[i]['title']
        st.info(f"🎥 {match} ({round(score*100)}% match)")
else:
    st.warning("Add at least 2 movies to enable AI recommendations.")