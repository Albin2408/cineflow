# 🎬 CineFlow: AI Movie Discovery & Tracking

CineFlow is a personal movie tracking and recommendation app that helps you discover, rate, and organize your movie collection. Get personalized recommendations based on movies you love, track your rewatches, and discover movies based on your mood.

## Features

- **🎯 Movie Search & Discovery** - Search TMDB and add movies to your collection or watchlist
- **⭐ Rating & Reviews** - Rate movies 0-10 with decimals (e.g., 9.5/10) and write personal reviews
- **😊 Mood Tagging** - Tag movies with emotions (Happy, Sad, Scary, Action, etc.)
- **🎯 Mood-Based Search** - Discover movies based on how you want to feel
- **🔄 Rewatch Tracking** - Track how many times you've rewatched each movie
- **📊 Stats & Wrap-Ups** - Monthly and yearly statistics with downloadable reports
- **📌 Watchlist** - Maintain a queue of movies you want to watch
- **🍿 AI Recommendations** - Get personalized recommendations based on your collection
- **📺 Movie Posters** - Browse movies with their official TMDB posters

## Prerequisites

- Python 3.8+
- TMDB API Key (free at [themoviedb.org](https://www.themoviedb.org/api))

## Installation

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd cineflow
```

### 2. Create a virtual environment
```bash
python -m venv venv
```

### 3. Activate the virtual environment

**On Windows:**
```bash
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Set up environment variables
Create a `.env` file in the project root:
```
TMDB_API_KEY=your_api_key_here
```

To get your TMDB API key:
1. Go to https://www.themoviedb.org/
2. Create an account (if you don't have one)
3. Go to Settings → API
4. Request an API key
5. Copy your API key and paste it in `.env`

### 6. Initialize the database
```bash
python database_setup.py
```

### 7. Run the app
```bash
streamlit run web_app.py
```

The app will open in your browser at `http://localhost:8501`

## How to Use

### Adding Movies
1. Use the search box to find movies on TMDB
2. Choose "➕ Add to Collection" to track it, or "📌 Add to Watchlist" to watch later
3. Suggestions appear as you type!

### Rating & Reviewing
1. Select a movie from your collection
2. Rate it (0-10 scale), add a mood tag, and write a review
3. Click "💾 Save Rating & Review"

### Tracking Rewatches
1. When you watch a movie again, click "🔄 I Watched This Again"
2. Your rewatch count updates automatically
3. See all rewatches in the collection sidebar

### Discovering by Mood
1. Go to "🎯 Search by Mood"
2. Select a mood (Happy, Sad, Scary, etc.)
3. Browse recommendations and add to your collection

### Viewing Stats
1. Check "📊 Your Stats & Wrap-Ups"
2. See monthly and yearly statistics
3. View your top 5 most-rewatched movies
4. Download wrap-up reports as text files

## File Structure

```
cineflow/
├── app.py                    # CLI version (optional)
├── web_app.py               # Main Streamlit app
├── database_setup.py        # Database initialization
├── recommend.py             # Recommendation logic
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (not in repo)
├── .gitignore              # Git ignore rules
├── README.md               # This file
└── cineflow.db             # SQLite database (not in repo)
```

## Database Schema

- **movies** - Your movie collection (title, rating, poster, watch count, etc.)
- **ratings** - Movie ratings, reviews, and mood tags
- **watchlist** - Movies you want to watch

## Technologies Used

- **Streamlit** - Web frontend
- **SQLite** - Local database
- **TMDB API** - Movie data and recommendations
- **Pandas** - Data manipulation
- **Scikit-learn** - ML-based recommendations
- **Python-dotenv** - Environment variable management

## Tips & Tricks

- 💡 **Mood Search** works best when you're not sure what to watch but know how you want to feel
- 📊 **Wrap-ups** automatically calculate stats from rated movies (movies without ratings don't count)
- 🎯 **Recommendations** use TMDB's algorithm plus the movies in your collection
- 📌 **Watchlist** is separate from your collection—move things over once you watch them!

## Troubleshooting

**"ModuleNotFoundError: No module named 'requests'"**
- Make sure you've installed the requirements: `pip install -r requirements.txt`

**"No TMDB_API_KEY found"**
- Check that your `.env` file exists and has your API key set correctly

**"Failed to save rating"**
- Delete `cineflow.db` and run `python database_setup.py` to recreate the database

**Movies aren't showing up in search**
- Make sure your TMDB API key is valid and working
- Check that you're typing at least 2 characters in the search box

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to fork this project and submit pull requests with improvements!

## Support

If you encounter any issues, please open an issue on GitHub.

---

**Happy watching! 🍿** 

Made with ❤️ for movie lovers everywhere.
