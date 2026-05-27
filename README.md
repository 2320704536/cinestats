# CineStats — Film Festival Analytics

A cinematic Streamlit dashboard for exploring live movie data from TMDb.  
CineStats turns film metadata into an interactive research archive, combining popular releases, top-rated cinema, director analytics, genre patterns, audience ratings, popularity signals, and movie search inside a 35mm-inspired visual interface.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive_Charts-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![TMDb](https://img.shields.io/badge/TMDb-Live_Movie_Data-01B4E4?style=for-the-badge)

---

## Overview

CineStats is a film analytics web application designed for movie data exploration, festival-style curation, and cinematic research. It collects live data from [The Movie Database API](https://developer.themoviedb.org/docs), processes it with Pandas, and presents it through Streamlit and Plotly as a searchable, filterable, exportable dashboard.

The app is built around the atmosphere of a late-night data theater: dark projection-room backgrounds, cream-colored typography, archive-style grids, 35mm references, scene labels, red recording details, and gold highlights. Instead of feeling like a plain analytics table, the interface behaves like a curated film research archive.

---

## Key Features

- Live movie data from TMDb
- Popular movie analytics
- Top-rated movie exploration
- Director performance analysis
- Genre distribution charts
- Rating and popularity comparisons
- Release-year trend visualization
- Searchable movie archive
- Poster-based movie cards
- Interactive filters
- Exportable CSV datasets
- Custom cinematic CSS theme

---

## App Structure

The dashboard is organized into five cinematic scenes. Each tab focuses on a different analytical lens.

| Scene | Page | Purpose |
|---|---|---|
| Scene 01 | Overview | High-level metrics, genre distribution, top ratings, release-year trends, popularity analysis, and full movie table |
| Scene 02 | Directors | Director ranking, average ratings, film count, total revenue, director search, and director dataset export |
| Scene 03 | Popular | Popular movie list with genre and minimum-rating filters |
| Scene 04 | Canon | Top-rated film archive with year and genre filters |
| Scene 05 | Search | Live movie lookup by title using TMDb search |

---

## Scene 01 · Analytics Overview

The Overview page provides the main analytical snapshot of the movie archive.

It includes four headline metrics:

- Number of popular movies loaded
- Number of top-rated titles loaded
- Number of available movie categories
- Average rating across the top-rated dataset

It also includes several visualizations:

- **Category Distribution**  
  A donut chart showing the dominant genres among popular movies.

- **Top 10 Rated Films**  
  A horizontal bar chart ranking the highest-rated films.

- **Movies by Release Year**  
  A line chart showing how top-rated films are distributed across release years.

- **Average Rating by Category**  
  A genre-level comparison of average ratings.

- **Rating vs Popularity**  
  A scatter plot comparing audience rating, popularity, vote count, and genre.

The page also includes a full movie data table with filters for genre, release year, and minimum rating. The filtered result can be exported as a CSV file.

---

## Scene 02 · Director Ledger

The Directors page builds a focused ledger of directors represented in the top-rated movie dataset.

For each director, the app calculates:

- Number of movies in the dataset
- Average movie rating
- Best-rated movie
- Total reported revenue
- Director profile image, when available

The page includes:

- Top directors by average rating
- Most prolific directors by film count
- Rating vs total revenue scatter plot
- Director data table
- Minimum rating and movie-count filters
- Director name search
- CSV export for director analytics

This section gives the dashboard a stronger film-studies angle by moving beyond individual titles and into creative authorship.

---

## Scene 03 · Popular Titles

The Popular page focuses on movies currently receiving strong audience attention on TMDb.

Users can filter the popular movie dataset by:

- Movie category
- Minimum rating

Each result is displayed as an expandable movie card containing:

- Poster
- Title
- Release year
- Rating
- Genre list
- Popularity score
- Vote count
- Overview

This page is useful for quickly scanning what is currently trending and comparing audience response across popular releases.

---

## Scene 04 · Festival Canon

The Canon page presents the top-rated movie archive.

Users can filter the dataset by:

- Release year
- Genre

The page includes both a table view and expandable movie cards. This makes it useful for studying highly rated titles as if they were part of a festival program or curated cinema canon.

---

## Scene 05 · Archive Search

The Search page allows users to look up any movie title through TMDb.

When a user enters a query, the app:

1. Sends the search term to the TMDb movie search endpoint.
2. Converts the results into a structured DataFrame.
3. Displays a compact results table.
4. Renders the top results as expandable movie cards.

This turns the app into a lightweight movie archive browser in addition to a dashboard.

---

## Tech Stack

| Technology | Role |
|---|---|
| Streamlit | Builds the interactive web app |
| Pandas | Cleans, structures, filters, and exports movie data |
| Plotly Express | Creates interactive charts |
| Requests | Connects to the TMDb API |
| TMDb API | Provides live movie, genre, director, revenue, poster, and search data |
| Custom CSS | Creates the cinematic 35mm-inspired interface |

---

## Data Pipeline

The app follows a clear data flow:

```text
TMDb API
   ↓
requests
   ↓
JSON movie data
   ↓
Pandas DataFrame
   ↓
filters, charts, tables, cards
   ↓
Streamlit dashboard
```

Main data-processing steps:

1. Fetch popular and top-rated movie pages from TMDb.
2. Fetch the genre list and map genre IDs to readable names.
3. Convert raw movie records into a clean DataFrame.
4. Request movie details and credits for director analysis.
5. Build chart-ready datasets for genres, ratings, years, popularity, and directors.
6. Render visualizations, tables, cards, and CSV downloads in Streamlit.

---

## Main Functions

| Function | Description |
|---|---|
| `tmdb_get()` | Sends API requests to TMDb and handles request failures |
| `get_movies()` | Loads multiple pages of movies from a TMDb movie endpoint |
| `get_movie_bundle()` | Fetches movie details together with credits |
| `search_movies()` | Searches TMDb by movie title |
| `get_genre_list()` | Retrieves genre ID-to-name mappings |
| `build_df()` | Converts raw TMDb movie results into a Pandas DataFrame |
| `build_director_data()` | Builds director-level statistics from movie credits |
| `curated_chart()` | Applies the custom visual theme to Plotly charts |
| `render_movie_card()` | Displays an expandable movie detail card |

---

## Caching

The app uses Streamlit caching through `@st.cache_data` to improve performance and reduce repeated API calls.

Cached functions include:

- `get_movies()`
- `get_movie_bundle()`
- `search_movies()`
- `get_genre_list()`
- `build_director_data()`

This is especially important for the director page, because it needs additional requests for movie credits and metadata.

---

## Visual Design

CineStats is styled as a cinematic research archive rather than a generic dashboard.

The interface uses:

- Dark projection-room background
- Cream-colored text inspired by archival paper and film labels
- Gold accents for key highlights
- Red REC indicator for a camera-monitor feel
- 35mm typography as a film-format reference
- Thin archive-grid background
- Scene-based navigation
- Monospace labels inspired by slate boards and technical notes
- Large condensed display typography for the main title

Fonts used:

- Archivo Black
- IBM Plex Mono
- Inter

The design language matches the app content: film history, live cinema data, festival programming, and archive-style research.

---

## Recommended Project Structure

```text
cinestats/
├── app.py
├── README.md
├── requirements.txt
└── .streamlit/
    └── secrets.toml
```

Recommended file roles:

- `app.py` contains the Streamlit application.
- `README.md` documents the project.
- `requirements.txt` lists Python dependencies.
- `.streamlit/secrets.toml` stores the TMDb API key.

---

## Installation

### 1. Create a project folder

```bash
mkdir cinestats
cd cinestats
```

Save the application code as:

```text
app.py
```

### 2. Create and activate a virtual environment

macOS or Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install streamlit pandas plotly requests
```

Or create a `requirements.txt` file:

```txt
streamlit
pandas
plotly
requests
```

Then install with:

```bash
pip install -r requirements.txt
```

---

## TMDb API Key Setup

This app requires a TMDb API key.

Create the following file:

```text
.streamlit/secrets.toml
```

Add your key:

```toml
TMDB_API_KEY = "your_tmdb_api_key_here"
```

If the key is missing, the app will stop and show:

```text
Missing `TMDB_API_KEY` in Streamlit secrets.
```

---

## How to Get a TMDb API Key

1. Go to [The Movie Database](https://www.themoviedb.org/).
2. Create an account or log in.
3. Open your account settings.
4. Go to the API section.
5. Apply for an API key.
6. Copy the v3 API key into `.streamlit/secrets.toml`.

---

## Run the App

```bash
streamlit run app.py
```

Streamlit will start a local development server, usually at:

```text
http://localhost:8501
```

---

## TMDb Endpoints Used

| Endpoint | Purpose |
|---|---|
| `/movie/popular` | Loads popular movies |
| `/movie/top_rated` | Loads top-rated movies |
| `/movie/{movie_id}` | Loads individual movie details |
| `/movie/{movie_id}?append_to_response=credits` | Loads movie details and credits |
| `/search/movie` | Searches for movies by title |
| `/genre/movie/list` | Loads genre ID mappings |

Because the data comes from TMDb, ratings, popularity, vote counts, revenue, overviews, and search results may change over time.

---

## Exported Data

The app supports CSV export for:

- Filtered movie table from the Overview page
- Director analytics table from the Directors page
- Top-rated movie dataset from the bottom export button

These exports are useful for further analysis, reports, coursework, or presentation materials.

---

## Notes and Limitations

- Do not commit your TMDb API key to a public repository.
- Add `.streamlit/secrets.toml` to `.gitignore`.
- Some movies may not include posters, overviews, revenue, or director profile images.
- Revenue data is not available for every film.
- Director analytics may take longer to load because credits are fetched separately.
- Search results and popular movie rankings depend on TMDb's current data.
- The app currently uses English-language TMDb results through `language="en-US"`.

---

## Future Improvements

Possible next steps:

- Add a dedicated movie detail page
- Add actor-level analytics
- Add country and language breakdowns
- Add budget, revenue, and profit analysis
- Add date-range filters
- Add user-created watchlists
- Add Streamlit Cloud deployment notes
- Add more advanced festival-programming views
- Add chart theme switching
- Add clearer API error messages

---

## Credits

This project uses data from [The Movie Database API](https://developer.themoviedb.org/docs).  
This product uses the TMDb API but is not endorsed or certified by TMDb.

---

## License

This project can be released under the MIT License or adjusted to match course, school, or team requirements.
