import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_recommendations():
    # 1. Pull data from your SQL database
    conn = sqlite3.connect('cineflow.db')
    df = pd.read_sql_query("SELECT title, overview FROM movies", conn)
    conn.close()

    if len(df) < 2:
        print("Add more movies to your collection first!")
        return

    # 2. Convert text to math (TF-IDF)
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['overview'].fillna(''))

    # 3. Calculate similarity between all movies
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    # 4. Show results
    print("\n--- Similarity Analysis ---")
    for idx, row in df.iterrows():
        print(f"\nMovies similar to '{row['title']}':")
        # Get scores for this movie against all others
        sim_scores = list(enumerate(cosine_sim[idx]))
        # Sort by score (descending) and skip the first one (itself)
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        for i, score in sim_scores[1:3]: # Top 2 matches
            print(f" -> {df.iloc[i]['title']} (Match Score: {round(score*100)}%)")

if __name__ == "__main__":
    get_recommendations()