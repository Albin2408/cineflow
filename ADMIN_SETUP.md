# 🔐 Admin Dashboard Setup

## Setting Up Admin Access

The admin dashboard is now integrated into CineFlow! Here's how to configure it:

### 1. Set Admin Password

Open or create a `.env` file in your project root and add:

```
ADMIN_PASSWORD=your_secure_password_here
```

Replace `your_secure_password_here` with a strong password of your choice.

**Default password** (if not set): `admin123`

### 2. Access the Admin Dashboard

1. Start the web app: `streamlit run web_app.py`
2. In the sidebar, scroll down to find the **🔐 Admin Access** section
3. Enter your admin password and click "🔓 Login as Admin"
4. Once authenticated, a new **🔐 Admin Dashboard** section appears below the main content

## Admin Dashboard Features

### 📊 Overview Tab
- **Collection Statistics**: Total movies, average rating, rewatches, watchlist items
- **Monthly Activity Chart**: See rating trends over the last 12 months

### ⭐ Ratings Analysis Tab
- **Top 10 Highest-Rated Movies**: Visual bar chart + detailed data
- **Top 10 Lowest-Rated Movies**: Find movies that underperformed
- **Rating Distribution**: Histogram showing how ratings are spread

### 👁️ Viewing Stats Tab
- **Most Rewatched Movies**: See which movies are watched repeatedly
- **Rewatch Count Details**: Full list of rewatch statistics

### 😊 Mood Insights Tab
- **Mood Distribution**: See which moods are most common in ratings
- **Mood Pie Chart**: Visual breakdown of mood percentages
- **Detailed Mood Statistics**: Raw data for mood analysis

### 📥 Data Export Tab
- Export **All Ratings** as CSV
- Export **Top Rated Movies** as CSV
- Export **Most Watched Movies** as CSV
- Export **Mood Analysis** as CSV
- Export **Full Database** (movies, ratings, watchlist tables separately)

## Use Cases for Business Owners

✅ **Engagement Metrics** - See which movies users interact with most
✅ **Mood Trends** - Understand what emotional content resonates
✅ **Quality Control** - Identify highest and lowest-rated titles
✅ **Rewatch Patterns** - Track beloved movies that drive repeat engagement
✅ **Monthly Reports** - Export data for business analysis and reports
✅ **Growth Tracking** - Monitor collection growth over time

## Security Notes

- The admin password is read from the `.env` file
- Never commit sensitive passwords to version control
- Add `.env` to your `.gitignore` file
- Change the password regularly in production environments
