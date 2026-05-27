# 🎬 CineStats — Film Festival Analytics

**CineStats** is a real-time film data analytics dashboard built with **Streamlit**, **Plotly**, **Pandas**, and the **TMDb API**.

Created by **WANG XINRU**  
For **Arts and Big Data**  
Sungkyunkwan University | 2026 Spring

---

## 📌 Project Overview

**CineStats** is an interactive web application that explores film data through a cinematic-style dashboard.

The project uses real-time movie data from **The Movie Database (TMDb)** API and transforms it into visual insights, including movie ratings, popularity, genre distribution, release year trends, director performance, and search results.

Instead of presenting movie information only as plain text or lists, CineStats uses charts, filters, tables, posters, and movie cards to help users understand patterns behind films and audience preferences.

---

## ✨ Main Features

### 📊 Analytics Overview

- Displays key movie statistics
- Shows genre/category distribution
- Visualizes top-rated films
- Analyzes movie release year trends
- Compares ratings and popularity through scatter plots
- Provides an interactive full movie data table

### 🎬 Director Analysis

- Analyzes directors from top-rated movie data
- Shows top directors by average rating
- Displays directors by number of films
- Compares director rating and total revenue
- Includes director detail search
- Supports director data export as CSV

### 🔥 Popular Movies

- Displays currently popular films from TMDb
- Supports genre/category filtering
- Supports minimum rating filtering
- Shows movie posters, ratings, popularity, votes, and overviews

### 🏆 Top Rated Movies

- Displays top-rated films from TMDb
- Supports filtering by year and genre
- Provides both table view and detailed movie cards

### 🔍 Movie Search

- Allows users to search movie titles in real time
- Shows search results in table format
- Displays detailed movie cards with poster, rating, votes, genre, and overview

### 📤 CSV Export

Users can download:

- Filtered movie data
- Director data
- Top-rated movie data

---

## 🛠️ Tools and Technologies

| Tool | Purpose |
|---|---|
| **Python** | Main programming language |
| **Streamlit** | Web application framework |
| **Pandas** | Data cleaning and table processing |
| **Plotly Express** | Interactive data visualization |
| **Requests** | API data fetching |
| **TMDb API** | Real-time movie data source |

---

## 📊 Data Source

This project uses data from **The Movie Database (TMDb) API**.

The app retrieves movie and director information in real time, including:

| Data Type | Description |
|---|---|
| Movie Title | Film name |
| Release Year | Year of release |
| Rating | TMDb user rating |
| Vote Count | Number of user votes |
| Popularity | TMDb popularity score |
| Genre | Movie category information |
| Overview | Short movie description |
| Poster | Movie poster image |
| Director | Director name and filmography |
| Revenue | Box office revenue data |

No static dataset is used. Data is fetched live during each app session.

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

This app requires a TMDb API key.

Create a `.streamlit/secrets.toml` file in your project folder:

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

Create a `requirements.txt` file with:

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

The main purpose of CineStats is to show how data analysis and visualization can be applied to film and media studies. By combining real-time movie data with interactive charts, the app helps users explore the relationship between ratings, popularity, genres, release years, and director performance.

Through this project, I wanted to demonstrate that data is not only useful in business or science, but can also support creative fields such as cinema. CineStats connects film culture, audience response, and visual storytelling through a digital data dashboard.

---

## 💡 What I Learned

Through building this project, I learned how to:

- Use APIs to collect real-time data
- Clean and organize movie data with Pandas
- Create interactive visualizations with Plotly
- Build a web app using Streamlit
- Design a dashboard with both functional and visual elements
- Connect film studies with data analysis

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

**CineStats — Film Festival Analytics** is a project that connects film, data, and visual storytelling.
