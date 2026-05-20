import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="CineStats — Film Festival Analytics",
    page_icon="🎬",
    layout="wide"
)

# ─────────────────────────────────────────────
# API Settings
# ─────────────────────────────────────────────
API_KEY = st.secrets["TMDB_API_KEY"]
BASE_URL = "https://api.themoviedb.org/3"

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
        --bg-main: #071019;
        --bg-deep: #0b1621;
        --bg-panel: rgba(16, 29, 43, 0.82);
        --bg-panel-strong: rgba(18, 34, 50, 0.92);
        --bg-soft: rgba(255, 255, 255, 0.035);
        --line-soft: rgba(143, 183, 209, 0.16);
        --line-gold: rgba(199, 165, 106, 0.34);
        --text-main: #f2eee6;
        --text-soft: #aab6c4;
        --text-faint: rgba(170, 182, 196, 0.68);
        --gold: #c7a56a;
        --gold-deep: #8f7650;
        --silver: #8fb7d1;
        --silver-bright: #c9dceb;
        --shadow-deep: 0 28px 80px rgba(0, 0, 0, 0.42);
        --shadow-soft: 0 18px 40px rgba(0, 0, 0, 0.28);
        --radius-xl: 30px;
        --radius-lg: 22px;
        --radius-md: 16px;
        --radius-sm: 12px;
    }

    html, body, [class*="css"] {
        font-family: "Manrope", sans-serif;
    }

    .stApp {
        color: var(--text-main);
        background:
            radial-gradient(circle at 12% 8%, rgba(143, 183, 209, 0.10), transparent 24%),
            radial-gradient(circle at 84% 14%, rgba(199, 165, 106, 0.10), transparent 20%),
            radial-gradient(circle at 50% 100%, rgba(95, 131, 160, 0.08), transparent 28%),
            linear-gradient(145deg, #04070b 0%, #071019 38%, #0a1520 68%, #0d1b2a 100%);
        background-attachment: fixed;
    }

    .block-container {
        max-width: 1240px;
        padding-top: 2.2rem;
        padding-bottom: 3.2rem;
    }

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(180deg, rgba(8, 15, 24, 0.98) 0%, rgba(12, 23, 36, 0.98) 100%);
        border-right: 1px solid var(--line-soft);
        box-shadow: inset -1px 0 0 rgba(199, 165, 106, 0.08);
    }

    section[data-testid="stSidebar"] * {
        color: var(--text-main);
    }

    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span {
        color: var(--text-soft);
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 2.8rem 2.5rem 2.6rem 2.5rem;
        margin-bottom: 1.7rem;
        border-radius: var(--radius-xl);
        border: 1px solid rgba(143, 183, 209, 0.18);
        background:
            linear-gradient(135deg, rgba(255,255,255,0.04), rgba(255,255,255,0.015)),
            linear-gradient(120deg, rgba(10, 19, 30, 0.92), rgba(14, 29, 44, 0.88) 58%, rgba(18, 38, 56, 0.92));
        box-shadow: var(--shadow-deep);
        backdrop-filter: blur(10px);
    }

    .hero::before {
        content: "";
        position: absolute;
        inset: 0;
        background:
            linear-gradient(90deg, rgba(199,165,106,0.10), transparent 28%),
            linear-gradient(180deg, transparent, rgba(143,183,209,0.08));
        pointer-events: none;
    }

    .hero::after {
        content: "";
        position: absolute;
        width: 340px;
        height: 340px;
        right: -110px;
        top: -120px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(201,220,235,0.10), rgba(143,183,209,0.04) 36%, transparent 68%);
        filter: blur(8px);
        pointer-events: none;
    }

    .festival-label {
        display: inline-flex;
        align-items: center;
        gap: 0.55rem;
        margin-bottom: 0.8rem;
        color: var(--gold);
        font-size: 0.76rem;
        font-weight: 800;
        letter-spacing: 0.22em;
        text-transform: uppercase;
    }

    .festival-label::before {
        content: "";
        width: 38px;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--gold));
    }

    .hero-title {
        font-family: "Cormorant Garamond", serif;
        font-size: 4rem;
        line-height: 0.95;
        font-weight: 700;
        letter-spacing: 0.01em;
        color: var(--text-main);
        margin-bottom: 0.75rem;
        text-shadow: 0 6px 30px rgba(0, 0, 0, 0.22);
    }

    .hero-subtitle {
        max-width: 760px;
        font-size: 1rem;
        line-height: 1.8;
        color: var(--text-soft);
        letter-spacing: 0.01em;
    }

    .section-title {
        display: flex;
        align-items: center;
        gap: 0.85rem;
        margin-top: 1.5rem;
        margin-bottom: 0.55rem;
        color: var(--text-main);
        font-family: "Cormorant Garamond", serif;
        font-size: 2rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }

    .section-title::before {
        content: "";
        width: 44px;
        height: 1px;
        background: linear-gradient(90deg, var(--gold), rgba(143,183,209,0.28));
        flex-shrink: 0;
    }

    .section-caption {
        margin-bottom: 1rem;
        color: var(--text-faint);
        font-size: 0.95rem;
        line-height: 1.7;
    }

    hr {
        border: none;
        height: 1px;
        margin: 1.6rem 0;
        background: linear-gradient(90deg, transparent, rgba(199,165,106,0.34), rgba(143,183,209,0.24), transparent);
    }

    button[data-baseweb="tab"] {
        min-height: 48px;
        padding: 0.55rem 1.05rem;
        margin-right: 0.55rem;
        border-radius: 999px;
        border: 1px solid rgba(143, 183, 209, 0.14);
        background: rgba(255, 255, 255, 0.025);
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.04);
        transition: all 0.22s ease;
    }

    button[data-baseweb="tab"] p {
        color: var(--text-soft);
        font-weight: 700;
        letter-spacing: 0.01em;
    }

    button[data-baseweb="tab"]:hover {
        border-color: rgba(199, 165, 106, 0.25);
        background: rgba(255,255,255,0.045);
        transform: translateY(-1px);
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        border: 1px solid rgba(199, 165, 106, 0.34);
        background:
            linear-gradient(135deg, rgba(199,165,106,0.18), rgba(143,183,209,0.08)),
            rgba(255,255,255,0.04);
        box-shadow:
            inset 0 1px 0 rgba(255,255,255,0.06),
            0 10px 26px rgba(0,0,0,0.18);
    }

    button[data-baseweb="tab"][aria-selected="true"] p {
        color: var(--text-main);
    }

    div[data-testid="stMetric"] {
        padding: 1.15rem 1.15rem 1rem 1.15rem;
        border-radius: var(--radius-lg);
        border: 1px solid rgba(143, 183, 209, 0.14);
        background:
            linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02)),
            var(--bg-panel);
        box-shadow: var(--shadow-soft);
        backdrop-filter: blur(8px);
    }

    div[data-testid="stMetricLabel"] {
        color: var(--text-faint);
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }

    div[data-testid="stMetricValue"] {
        color: var(--text-main);
        font-family: "Cormorant Garamond", serif;
        font-size: 2.2rem;
        font-weight: 700;
        letter-spacing: 0.02em;
    }

    div[data-testid="stMetricDelta"] {
        color: var(--silver) !important;
    }

    div[data-testid="stExpander"] {
        border-radius: var(--radius-md);
        border: 1px solid rgba(143, 183, 209, 0.12);
        background:
            linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.018)),
            rgba(13, 25, 38, 0.72);
        box-shadow: 0 14px 30px rgba(0, 0, 0, 0.18);
        overflow: hidden;
    }

    div[data-testid="stExpander"] summary {
        color: var(--text-main);
        font-weight: 800;
        padding-top: 0.1rem;
        padding-bottom: 0.1rem;
    }

    .stButton > button,
    .stDownloadButton > button {
        min-height: 46px;
        padding: 0.65rem 1.15rem;
        border-radius: 999px;
        border: 1px solid rgba(199, 165, 106, 0.34);
        background:
            linear-gradient(135deg, rgba(199,165,106,0.20), rgba(143,183,209,0.08)),
            rgba(255,255,255,0.04);
        color: var(--text-main);
        font-weight: 800;
        letter-spacing: 0.01em;
        box-shadow:
            inset 0 1px 0 rgba(255,255,255,0.05),
            0 12px 30px rgba(0,0,0,0.2);
        transition: all 0.22s ease;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        border-color: rgba(199, 165, 106, 0.52);
        box-shadow:
            inset 0 1px 0 rgba(255,255,255,0.07),
            0 18px 34px rgba(0,0,0,0.24);
        color: #ffffff;
    }

    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea,
    div[data-baseweb="select"] > div,
    div[data-baseweb="base-input"] {
        border-radius: 14px !important;
        border: 1px solid rgba(143, 183, 209, 0.14) !important;
        background: rgba(10, 19, 29, 0.82) !important;
        color: var(--text-main) !important;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.03);
    }

    .stTextInput input:focus,
    .stNumberInput input:focus,
    .stTextArea textarea:focus {
        border-color: rgba(199, 165, 106, 0.34) !important;
        box-shadow: 0 0 0 1px rgba(199, 165, 106, 0.18) !important;
    }

    label,
    .stSlider label,
    .stMultiSelect label,
    .stSelectbox label {
        color: var(--text-soft) !important;
        font-weight: 700;
        letter-spacing: 0.01em;
    }

    .stSlider [data-baseweb="slider"] > div > div {
        background: linear-gradient(90deg, var(--gold), var(--silver)) !important;
    }

    .stSlider [role="slider"] {
        background: var(--silver-bright) !important;
        border: 2px solid var(--bg-main) !important;
        box-shadow: 0 0 0 4px rgba(143,183,209,0.12);
    }

    .stDataFrame,
    div[data-testid="stTable"] {
        border-radius: 18px;
        overflow: hidden;
        border: 1px solid rgba(143, 183, 209, 0.12);
        box-shadow: var(--shadow-soft);
    }

    div[data-testid="stDataFrame"] div[role="table"] {
        background: rgba(10, 19, 29, 0.72);
    }

    div[data-testid="stDataFrame"] [role="columnheader"] {
        background: rgba(199, 165, 106, 0.10);
        color: var(--text-main);
        font-weight: 800;
        border-bottom: 1px solid rgba(199, 165, 106, 0.12);
    }

    div[data-testid="stDataFrame"] [role="gridcell"] {
        color: var(--text-soft);
        border-bottom: 1px solid rgba(143, 183, 209, 0.06);
    }

    .stCaption,
    .stMarkdown p,
    .stMarkdown li {
        color: var(--text-soft);
    }

    .stAlert {
        border-radius: 16px;
        border: 1px solid rgba(143, 183, 209, 0.16);
        background: rgba(11, 21, 32, 0.78);
        color: var(--text-main);
    }

    .gold-text {
        color: var(--gold);
        font-weight: 800;
        letter-spacing: 0.01em;
    }

    .stPlotlyChart {
        border-radius: 22px;
        padding: 0.4rem;
        background:
            linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.015)),
            rgba(9, 17, 26, 0.52);
        border: 1px solid rgba(143, 183, 209, 0.10);
        box-shadow: var(--shadow-soft);
    }

    [data-testid="stImage"] img {
        border-radius: 14px;
        border: 1px solid rgba(143, 183, 209, 0.12);
        box-shadow: 0 14px 28px rgba(0,0,0,0.25);
    }

    .st-emotion-cache-1kyxreq,
    .st-emotion-cache-ocqkz7 {
        gap: 1rem;
    }

    @media (max-width: 900px) {
        .block-container {
            padding-top: 1.4rem;
            padding-bottom: 2.2rem;
        }

        .hero {
            padding: 2rem 1.4rem 1.9rem 1.4rem;
            border-radius: 24px;
        }

        .hero-title {
            font-size: 3rem;
        }

        .hero-subtitle {
            font-size: 0.96rem;
            line-height: 1.7;
        }

        .section-title {
            font-size: 1.6rem;
        }
    }
</style>
""", unsafe_allow_html=True)
# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="festival-label">Film Festival Data Hub</div>
    <div class="hero-title">🎬 CineStats</div>
    <div class="hero-subtitle">
        An elegant film analytics dashboard exploring popular movies, top-rated films,
        directors, audience ratings, and movie trends using real-time TMDb data.
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# API Functions
# ─────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def get_movies(endpoint, pages=10):
    movies = []
    for page in range(1, pages + 1):
        r = requests.get(
            f"{BASE_URL}/movie/{endpoint}",
            params={"api_key": API_KEY, "language": "en-US", "page": page}
        )
        if r.status_code == 200:
            movies.extend(r.json().get("results", []))
    return movies

@st.cache_data(show_spinner=False)
def get_movie_credits(movie_id):
    r = requests.get(
        f"{BASE_URL}/movie/{movie_id}/credits",
        params={"api_key": API_KEY}
    )
    if r.status_code == 200:
        return r.json()
    return {}

@st.cache_data(show_spinner=False)
def get_movie_details(movie_id):
    r = requests.get(
        f"{BASE_URL}/movie/{movie_id}",
        params={"api_key": API_KEY, "language": "en-US"}
    )
    if r.status_code == 200:
        return r.json()
    return {}

@st.cache_data(show_spinner=False)
def search_movies(query):
    r = requests.get(
        f"{BASE_URL}/search/movie",
        params={"api_key": API_KEY, "language": "en-US", "query": query}
    )
    if r.status_code == 200:
        return r.json().get("results", [])
    return []

@st.cache_data(show_spinner=False)
def get_genre_list():
    r = requests.get(
        f"{BASE_URL}/genre/movie/list",
        params={"api_key": API_KEY, "language": "en-US"}
    )
    if r.status_code == 200:
        genres = r.json().get("genres", [])
        return {g["id"]: g["name"] for g in genres}
    return {}

# ─────────────────────────────────────────────
# Load Data
# ─────────────────────────────────────────────
with st.spinner("🎞️ Preparing your film festival dashboard..."):
    popular   = get_movies("popular", 10)
    top_rated = get_movies("top_rated", 10)
    genre_map = get_genre_list()

def build_df(movies):
    rows = []
    for m in movies:
        genres = [genre_map.get(gid, "Unknown") for gid in m.get("genre_ids", [])]
        rows.append({
            "ID":           m.get("id"),
            "Title":        m.get("title", "N/A"),
            "Release Year": m.get("release_date", "N/A")[:4] if m.get("release_date") else "N/A",
            "Rating":       m.get("vote_average", 0),
            "Votes":        m.get("vote_count", 0),
            "Popularity":   round(m.get("popularity", 0), 1),
            "Genre":        genres[0] if genres else "Unknown",
            "All Genres":   ", ".join(genres),
            "Overview":     m.get("overview", ""),
            "Poster":       f"https://image.tmdb.org/t/p/w200{m['poster_path']}" if m.get("poster_path") else ""
        })
    return pd.DataFrame(rows)

df_popular = build_df(popular)
df_top     = build_df(top_rated)

# ─────────────────────────────────────────────
# Chart Theme
# ─────────────────────────────────────────────
def festival_chart(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#f8f3e8",
        title_font_color="#ffffff",
        legend_title_text="",
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

# ─────────────────────────────────────────────
# Tabs
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Analytics",
    "🎬 Director Analysis",
    "🔥 Popular",
    "⭐ Top Rated",
    "🔍 Search"
])

# ─────────────────────────────────────────────
# Tab 1: Analytics
# ─────────────────────────────────────────────
with tab1:
    st.markdown('<div class="section-title">📊 Movie Analytics Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-caption">A quick overview of movie ratings, popularity, release years, and film categories.</div>', unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("🎬 Popular Movies",  len(df_popular))
    m2.metric("⭐ Top Rated",       len(df_top))
    m3.metric("🎭 Categories",      len(genre_map))
    m4.metric("📈 Avg Rating",      round(df_top["Rating"].mean(), 2))

    st.markdown("---")

    ch1, ch2 = st.columns(2)
    with ch1:
        st.markdown("### 🎭 Category Distribution")
        genre_count = df_popular["Genre"].value_counts().reset_index()
        genre_count.columns = ["Category", "Count"]
        fig1 = px.pie(genre_count, names="Category", values="Count", hole=0.45,
                      color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(festival_chart(fig1), use_container_width=True)

    with ch2:
        st.markdown("### ⭐ Top 10 Rated Movies")
        top10 = df_top.sort_values("Rating", ascending=False).head(10)
        fig2 = px.bar(top10, x="Rating", y="Title", orientation="h",
                      color="Rating", color_continuous_scale=["#27374d", "#d4af37"],
                      range_x=[0, 10])
        fig2.update_layout(yaxis_title="", xaxis_title="Rating")
        st.plotly_chart(festival_chart(fig2), use_container_width=True)

    ch3, ch4 = st.columns(2)
    with ch3:
        st.markdown("### 📅 Movies by Release Year")
        year_df = df_top[df_top["Release Year"] != "N/A"].copy()
        year_count = year_df["Release Year"].value_counts().sort_index().reset_index()
        year_count.columns = ["Year", "Count"]
        fig3 = px.line(year_count, x="Year", y="Count", markers=True,
                       color_discrete_sequence=["#d4af37"])
        fig3.update_traces(line=dict(width=3), marker=dict(size=8))
        st.plotly_chart(festival_chart(fig3), use_container_width=True)

    with ch4:
        st.markdown("### 🎯 Average Rating by Category")
        avg_genre = df_top.groupby("Genre")["Rating"].mean().round(2).reset_index()
        avg_genre.columns = ["Category", "Avg Rating"]
        avg_genre = avg_genre.sort_values("Avg Rating", ascending=False)
        fig4 = px.bar(avg_genre, x="Category", y="Avg Rating",
                      color="Avg Rating", color_continuous_scale=["#27374d", "#d4af37"],
                      range_y=[0, 10])
        fig4.update_layout(xaxis_title="", yaxis_title="Average Rating")
        st.plotly_chart(festival_chart(fig4), use_container_width=True)

    st.markdown("### 📈 Rating vs Popularity")
    fig5 = px.scatter(df_popular, x="Popularity", y="Rating",
                      hover_name="Title", color="Genre", size="Votes",
                      color_discrete_sequence=px.colors.qualitative.Set3)
    fig5.update_layout(xaxis_title="Popularity", yaxis_title="Rating")
    st.plotly_chart(festival_chart(fig5), use_container_width=True)

    # ── Data Table ────────────────────────────
    st.markdown("---")
    st.markdown("### 📋 Full Movie Data Table")
    st.markdown('<div class="section-caption">Filter, sort, and explore the complete dataset.</div>', unsafe_allow_html=True)

    tbl1, tbl2, tbl3 = st.columns(3)
    with tbl1:
        tbl_genre = st.multiselect("Filter by Genre", options=sorted(df_popular["Genre"].unique()), key="tbl_genre")
    with tbl2:
        tbl_year = st.multiselect("Filter by Year", options=sorted(df_popular["Release Year"].unique(), reverse=True), key="tbl_year")
    with tbl3:
        tbl_min_rating = st.slider("Min Rating", 0.0, 10.0, 0.0, 0.1, key="tbl_rating")

    df_table = df_popular.copy()
    if tbl_genre:
        df_table = df_table[df_table["Genre"].isin(tbl_genre)]
    if tbl_year:
        df_table = df_table[df_table["Release Year"].isin(tbl_year)]
    df_table = df_table[df_table["Rating"] >= tbl_min_rating]
    df_table = df_table.sort_values("Rating", ascending=False).reset_index(drop=True)

    st.dataframe(
        df_table[["Title", "Release Year", "Genre", "All Genres", "Rating", "Votes", "Popularity"]],
        use_container_width=True,
        height=400
    )
    st.caption(f"Showing {len(df_table)} movies")

    csv_all = df_table.to_csv(index=False).encode("utf-8")
    st.download_button("📤 Export Table as CSV", csv_all, "cinestats_movies.csv", "text/csv")

# ─────────────────────────────────────────────
# Tab 2: Director Analysis
# ─────────────────────────────────────────────
with tab2:
    st.markdown('<div class="section-title">🎬 Director Analysis</div>', unsafe_allow_html=True)
    st.info("Fetching director data from TMDb. The first load may take a moment.")

    @st.cache_data(show_spinner=False)
    def build_director_data(movie_ids):
        director_stats = {}
        progress = st.progress(0)
        for i, mid in enumerate(movie_ids):
            credits = get_movie_credits(mid)
            details = get_movie_details(mid)
            crew = credits.get("crew", [])
            for person in crew:
                if person.get("job") == "Director":
                    name = person["name"]
                    rating  = details.get("vote_average", 0)
                    revenue = details.get("revenue", 0)
                    title   = details.get("title", "Unknown")
                    year    = details.get("release_date", "")[:4]
                    if name not in director_stats:
                        director_stats[name] = {
                            "Movies": [], "Ratings": [], "Revenue": [],
                            "Photo": f"https://image.tmdb.org/t/p/w200{person.get('profile_path')}" if person.get("profile_path") else ""
                        }
                    director_stats[name]["Movies"].append(f"{title} ({year})")
                    director_stats[name]["Ratings"].append(rating)
                    director_stats[name]["Revenue"].append(revenue)
            progress.progress((i + 1) / len(movie_ids))
        progress.empty()
        return director_stats

    top50_ids    = df_top.sort_values("Rating", ascending=False).head(50)["ID"].tolist()
    director_data = build_director_data(tuple(top50_ids))

    dir_rows = []
    for name, data in director_data.items():
        avg_rating  = round(sum(data["Ratings"]) / len(data["Ratings"]), 2)
        total_rev   = sum(data["Revenue"])
        movie_count = len(data["Movies"])
        best_movie  = data["Movies"][data["Ratings"].index(max(data["Ratings"]))]
        dir_rows.append({
            "Director":      name,
            "Movies Count":  movie_count,
            "Avg Rating":    avg_rating,
            "Best Movie":    best_movie,
            "Total Revenue": total_rev,
            "Photo":         data["Photo"]
        })

    df_dir = pd.DataFrame(dir_rows).sort_values("Avg Rating", ascending=False)

    d1, d2, d3 = st.columns(3)
    d1.metric("🎬 Directors Analyzed", len(df_dir))
    d2.metric("⭐ Highest Avg Rating", df_dir["Avg Rating"].max())
    d3.metric("🏆 Most Prolific", df_dir.sort_values("Movies Count", ascending=False).iloc[0]["Director"])

    st.markdown("---")

    dc1, dc2 = st.columns(2)
    with dc1:
        st.markdown("### 🏆 Top 15 Directors by Rating")
        top_dir = df_dir.head(15)
        fig_d1 = px.bar(top_dir, x="Avg Rating", y="Director", orientation="h",
                        color="Avg Rating", color_continuous_scale=["#27374d", "#d4af37"],
                        range_x=[0, 10])
        fig_d1.update_layout(yaxis_title="", xaxis_title="Average Rating")
        st.plotly_chart(festival_chart(fig_d1), use_container_width=True)

    with dc2:
        st.markdown("### 🎞️ Directors by Number of Movies")
        prolific = df_dir.sort_values("Movies Count", ascending=False).head(15)
        fig_d2 = px.bar(prolific, x="Movies Count", y="Director", orientation="h",
                        color="Movies Count", color_continuous_scale=["#27374d", "#d4af37"])
        fig_d2.update_layout(yaxis_title="", xaxis_title="Movie Count")
        st.plotly_chart(festival_chart(fig_d2), use_container_width=True)

    st.markdown("### 💰 Rating vs Total Revenue")
    df_dir_plot = df_dir[df_dir["Total Revenue"] > 0]
    fig_d3 = px.scatter(df_dir_plot, x="Avg Rating", y="Total Revenue",
                        hover_name="Director", size="Movies Count",
                        color="Avg Rating", color_continuous_scale=["#27374d", "#d4af37"],
                        labels={"Total Revenue": "Total Revenue (USD)"})
    st.plotly_chart(festival_chart(fig_d3), use_container_width=True)

    # ── Director Table ────────────────────────
    st.markdown("---")
    st.markdown("### 📋 Director Data Table")
    st.markdown('<div class="section-caption">Full list of directors sorted by average rating.</div>', unsafe_allow_html=True)

    dir_tbl1, dir_tbl2 = st.columns(2)
    with dir_tbl1:
        dir_min_rating = st.slider("Min Avg Rating", 0.0, 10.0, 0.0, 0.1, key="dir_rating")
    with dir_tbl2:
        dir_min_movies = st.slider("Min Movies Count", 1, 10, 1, 1, key="dir_movies")

    df_dir_tbl = df_dir[
        (df_dir["Avg Rating"] >= dir_min_rating) &
        (df_dir["Movies Count"] >= dir_min_movies)
    ].reset_index(drop=True)

    st.dataframe(
        df_dir_tbl[["Director", "Movies Count", "Avg Rating", "Best Movie", "Total Revenue"]],
        use_container_width=True,
        height=350
    )
    st.caption(f"Showing {len(df_dir_tbl)} directors")

    st.markdown("---")
    st.markdown("### 🔍 Director Detail Search")
    dir_search = st.text_input("Search a director name")
    if dir_search:
        result = df_dir[df_dir["Director"].str.contains(dir_search, case=False, na=False)]
        if len(result) > 0:
            for _, row in result.iterrows():
                with st.expander(f"🎬 {row['Director']} — ⭐ {row['Avg Rating']} avg"):
                    c1, c2 = st.columns([1, 3])
                    with c1:
                        if row["Photo"]:
                            st.image(row["Photo"], width=130)
                    with c2:
                        st.write(f"**Movies in Dataset:** {row['Movies Count']}")
                        st.write(f"**Average Rating:** {row['Avg Rating']}")
                        st.write(f"**Best Rated Work:** {row['Best Movie']}")
                        if row["Total Revenue"] > 0:
                            st.write(f"**Total Revenue:** ${row['Total Revenue']:,}")
        else:
            st.warning("Director not found in the current dataset.")

    csv_dir = df_dir.drop(columns=["Photo"]).to_csv(index=False).encode("utf-8")
    st.download_button("📤 Export Director Data as CSV", csv_dir, "cinestats_directors.csv", "text/csv")

# ─────────────────────────────────────────────
# Tab 3: Popular
# ─────────────────────────────────────────────
with tab3:
    st.markdown('<div class="section-title">🔥 Popular Movies Right Now</div>', unsafe_allow_html=True)

    f1, f2 = st.columns(2)
    with f1:
        genre_options = ["All"] + sorted(df_popular["Genre"].unique())
        genre_sel = st.selectbox("Filter by Category", genre_options)
    with f2:
        min_rating = st.slider("Minimum Rating", 0.0, 10.0, 5.0, 0.1)

    df_p = df_popular.copy()
    if genre_sel != "All":
        df_p = df_p[df_p["Genre"] == genre_sel]
    df_p = df_p[df_p["Rating"] >= min_rating]
    df_p = df_p.sort_values("Popularity", ascending=False).reset_index(drop=True)
    st.caption(f"Showing {len(df_p)} popular movies.")

    for _, row in df_p.head(20).iterrows():
        with st.expander(f"🎬 {row['Title']} ({row['Release Year']}) — ⭐ {row['Rating']}"):
            c1, c2 = st.columns([1, 4])
            with c1:
                if row["Poster"]:
                    st.image(row["Poster"], width=115)
            with c2:
                st.markdown(f"<span class='gold-text'>Category:</span> {row['All Genres']}", unsafe_allow_html=True)
                st.write(f"**Popularity:** {row['Popularity']}")
                st.write(f"**Votes:** {row['Votes']:,}")
                if row["Overview"]:
                    st.caption(row["Overview"][:260] + "...")

# ─────────────────────────────────────────────
# Tab 4: Top Rated
# ─────────────────────────────────────────────
with tab4:
    st.markdown('<div class="section-title">⭐ Top Rated Movies of All Time</div>', unsafe_allow_html=True)

    tr1, tr2 = st.columns(2)
    with tr1:
        year_options = ["All"] + sorted(df_top["Release Year"].unique(), reverse=True)
        year_sel = st.selectbox("Filter by Year", year_options)
    with tr2:
        genre_options_top = ["All"] + sorted(df_top["Genre"].unique())
        genre_sel_top = st.selectbox("Filter by Genre", genre_options_top, key="top_genre")

    df_t = df_top.copy()
    if year_sel != "All":
        df_t = df_t[df_t["Release Year"] == year_sel]
    if genre_sel_top != "All":
        df_t = df_t[df_t["Genre"] == genre_sel_top]
    df_t = df_t.sort_values("Rating", ascending=False).reset_index(drop=True)

    st.caption(f"Showing {len(df_t)} top-rated movies.")

    # ── Top Rated Table ───────────────────────
    st.markdown("### 📋 Top Rated Table View")
    st.dataframe(
        df_t[["Title", "Release Year", "Genre", "All Genres", "Rating", "Votes", "Popularity"]],
        use_container_width=True,
        height=350
    )
    st.caption(f"{len(df_t)} movies in this view")

    st.markdown("---")

    for _, row in df_t.head(20).iterrows():
        with st.expander(f"🏆 {row['Title']} ({row['Release Year']}) — {row['Rating']}/10"):
            c1, c2 = st.columns([1, 4])
            with c1:
                if row["Poster"]:
                    st.image(row["Poster"], width=115)
            with c2:
                st.markdown(f"<span class='gold-text'>Category:</span> {row['All Genres']}", unsafe_allow_html=True)
                st.write(f"**Votes:** {row['Votes']:,}")
                if row["Overview"]:
                    st.caption(row["Overview"][:260] + "...")

# ─────────────────────────────────────────────
# Tab 5: Search
# ─────────────────────────────────────────────
with tab5:
    st.markdown('<div class="section-title">🔍 Search Any Movie</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-caption">Search for a film title and explore its rating, poster, votes, and overview.</div>', unsafe_allow_html=True)

    query = st.text_input("Enter a movie title", placeholder="e.g. Inception, Parasite, La La Land...")

    if query:
        with st.spinner("Searching the film archive..."):
            results = search_movies(query)
        if results:
            df_s = build_df(results)
            st.success(f"Found {len(df_s)} results for '{query}'")

            st.markdown("### 📋 Search Results Table")
            st.dataframe(
                df_s[["Title", "Release Year", "Genre", "Rating", "Votes"]],
                use_container_width=True,
                height=300
            )
            st.markdown("---")

            for _, row in df_s.head(10).iterrows():
                with st.expander(f"🎬 {row['Title']} ({row['Release Year']}) — ⭐ {row['Rating']}"):
                    c1, c2 = st.columns([1, 4])
                    with c1:
                        if row["Poster"]:
                            st.image(row["Poster"], width=115)
                    with c2:
                        st.markdown(f"<span class='gold-text'>Category:</span> {row['All Genres']}", unsafe_allow_html=True)
                        st.write(f"**Votes:** {row['Votes']:,}")
                        if row["Overview"]:
                            st.caption(row["Overview"][:260] + "...")
        else:
            st.warning("No results found. Try another movie title.")

# ─────────────────────────────────────────────
# Export
# ─────────────────────────────────────────────
st.markdown("---")
csv = df_top.to_csv(index=False).encode("utf-8")
st.download_button(
    "📤 Export Top Rated Movies as CSV",
    csv,
    "cinestats_top_rated.csv",
    "text/csv",
    use_container_width=True
)
