# 🎬 CineStats — Film Festival Analytics

**CineStats** is a real-time film data analytics dashboard built with **Streamlit**, **Pandas**, **Plotly Express**, and the **TMDb API**.

Created by **WANG XINRU**  
For **Arts and Big Data**  
Sungkyunkwan University | 2026 Spring

---

## 📌 Project Overview

**CineStats — Film Festival Analytics** is an interactive movie data dashboard designed with a cinematic visual style.

The project uses real-time data from **The Movie Database (TMDb) API** to explore popular movies, top-rated films, directors, ratings, genres, popularity, vote counts, release years, and box office revenue. The app presents film data through interactive charts, tables, filters, movie cards, and director analysis.

The visual design of the app is inspired by a film archive and festival screening interface. It uses a dark cinematic layout, 35mm film references, scene-style section titles, poster images, and interactive visualizations to connect film culture with data analysis.

---

## ✨ Main Features

### Scene 01 · Overview

The first section provides a general analytics overview of movie data.

It includes:

- Total number of popular movies loaded
- Total number of top-rated titles loaded
- Number of movie categories from TMDb
- Average rating of top-rated movies
- Category distribution pie chart
- Top 10 rated films bar chart
- Movies by release year line chart
- Average rating by category bar chart
- Rating vs popularity scatter plot
- Full movie data table with filters
- CSV export for filtered movie data

Users can filter the movie table by:

- Genre
- Release year
- Minimum rating

---

### Scene 02 · Directors

The second section focuses on director analysis based on the top-rated movie dataset.

It includes:

- Number of directors analyzed
- Highest average director rating
- Most prolific director in the dataset
- Top 15 directors by average rating
- Directors by number of films
- Rating vs total revenue scatter plot
- Director data table
- Director detail search
- Director profile photo display when available
- CSV export for director data

Users can filter director data by:

- Minimum average rating
- Minimum movie count

---

### Scene 03 · Popular

The third section displays currently popular movies from TMDb.

It includes:

- Popular movie list
- Genre/category filter
- Minimum rating filter
- Movie poster display
- Movie rating
- Popularity score
- Vote count
- Movie overview

Each movie is shown as an expandable movie card.

---

### Scene 04 · Canon

The fourth section displays top-rated films from TMDb.

It includes:

- Top-rated movie table
- Movie cards for selected top-rated films
- Poster images
- Ratings
- Vote counts
- Popularity scores
- Movie descriptions

Users can filter top-rated films by:

- Release year
- Genre

---

### Scene 05 · Search

The fifth section allows users to search for any movie title in real time.

It includes:

- Movie title search bar
- Real-time TMDb search results
- Search results table
- Detailed movie cards
- Poster images
- Genre information
- Ratings
- Vote counts
- Movie overviews

Example searches include:

- Inception
- Parasite
- La La Land

---

## 🛠️ Tools and Technologies

| Tool | Purpose |
|---|---|
| **Python** | Main programming language |
| **Streamlit** | Web app framework and interface |
| **Pandas** | Data cleaning and table processing |
| **Plotly Express** | Interactive charts and data visualization |
| **Requests** | Fetching data from the TMDb API |
| **TMDb API** | Real-time movie, genre, director, rating, and revenue data |

---

## 📊 Data Source

This project uses data from **The Movie Database (TMDb) API**.

The app fetches data live during each session. It does not rely on a static dataset.

The app retrieves:

| Data Type | Description |
|---|---|
| Movie ID | TMDb movie identification number |
| Movie Title | Film title |
| Release Year | Year of release |
| Rating | TMDb user rating |
| Vote Count | Number of user votes |
| Popularity | TMDb popularity score |
| Genre | Main genre and full genre list |
| Overview | Short movie description |
| Poster | Movie poster image |
| Director | Director name from movie credits |
| Director Photo | Director profile image when available |
| Revenue | Box office revenue data when available |

---

## 🎨 Visual Design

CineStats uses a custom cinematic interface created with CSS inside Streamlit.

The design includes:

- Dark film-theater background
- 35mm film reference
- Scene-style section titles
- Cream, amber, red, and blue-toned visual palette
- Film archive style layout
- Poster-based movie cards
- Interactive Plotly charts
- Responsive layout for different screen sizes

The visual style is designed to make the dashboard feel more like a film festival archive than a traditional data table.

---

## 🚀 How to Run the Project

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_LINK
cd YOUR_REPOSITORY_NAME
```

### 2. Install required libraries

```bash
pip install -r requirements.txt
```

### 3. Add TMDb API Key

This project requires a TMDb API key.

Create a folder named `.streamlit` in your project directory.

Inside that folder, create a file named `secrets.toml`.

The structure should look like this:

```txt
CineStats/
│
├── app.py
├── requirements.txt
├── README.md
└── .streamlit/
    └── secrets.toml
```

In `secrets.toml`, add:

```toml
TMDB_API_KEY = "your_tmdb_api_key_here"
```

### 4. Run the Streamlit app

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal.

---

## 📦 Requirements

Create a `requirements.txt` file with the following libraries:

```txt
streamlit
pandas
plotly
requests
```

---

## 📁 Project Structure

```txt
CineStats/
│
├── app.py
├── requirements.txt
├── README.md
└── .streamlit/
    └── secrets.toml
```

---

## 📸 Screenshot

<img width="1466" height="567" alt="CineStats Screenshot" src="https://github.com/user-attachments/assets/cfed9b55-1802-46fa-82a6-4653ecfd51da" />

---

## 🎯 Project Purpose

This project was created for the **Arts and Big Data** course.

The purpose of CineStats is to show how data analysis can be used to study film and media culture. By using live movie data from TMDb, the app helps users explore how films are rated, how popular they are, which genres appear most often, how release years are distributed, and how directors perform within the selected dataset.

Through this project, I wanted to combine film studies with data visualization. CineStats demonstrates that data is not only useful for business or science, but can also help us understand creative industries, audience preferences, and cultural trends in cinema.

---

## 💡 What I Learned

Through this project, I learned how to:

- Build an interactive web app with Streamlit
- Fetch real-time data from an external API
- Use Streamlit secrets to protect API keys
- Clean and organize movie data with Pandas
- Create interactive charts with Plotly Express
- Design data tables with filters and sorting
- Build movie cards with posters and expandable details
- Analyze directors using credits and revenue data
- Export filtered data as CSV files
- Combine visual design with data storytelling

---

## ⚠️ Notes

This app requires a valid TMDb API key.  
If the API key is missing, the app will stop and show an error message.

The movie data may change over time because the app fetches live data from TMDb.

Director and revenue information may be unavailable for some movies depending on the data provided by TMDb.

---

## 🙋‍♀️ Author

**WANG XINRU**

Created for **Arts and Big Data**  
Sungkyunkwan University | 2026 Spring

---

## 🙏 Acknowledgement

This project uses movie data provided by **The Movie Database (TMDb) API**.

This project was created as a final project for the **Arts and Big Data** course.

---

## 🎬 Final Note

**CineStats — Film Festival Analytics** connects film, data, and visual storytelling through an interactive movie analytics dashboard.
