import pandas as pd
import plotly.express as px
import requests
import streamlit as st



BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w200"
REQUEST_TIMEOUT = 20

if "TMDB_API_KEY" not in st.secrets:
    st.error("Missing `TMDB_API_KEY` in Streamlit secrets.")
    st.stop()

API_KEY = st.secrets["TMDB_API_KEY"]

APP_CSS = '''
<style>
    @import url("https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap");

    :root {
        --bg-main: #071019;
        --bg-deep: #0b1621;
        --bg-panel: rgba(16, 29, 43, 0.82);
        --text-main: #f2eee6;
        --text-soft: #aab6c4;
        --text-faint: rgba(170, 182, 196, 0.68);
        --gold: #c7a56a;
        --silver: #8fb7d1;
        --silver-bright: #c9dceb;
        --line-soft: rgba(143, 183, 209, 0.16);
        --shadow-deep: 0 28px 80px rgba(0, 0, 0, 0.42);
        --shadow-soft: 0 18px 40px rgba(0, 0, 0, 0.28);
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
        background: linear-gradient(180deg, rgba(8, 15, 24, 0.98) 0%, rgba(12, 23, 36, 0.98) 100%);
        border-right: 1px solid var(--line-soft);
        box-shadow: inset -1px 0 0 rgba(199, 165, 106, 0.08);
    }

    section[data-testid="stSidebar"] * {
        color: var(--text-main);
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 2.8rem 2.5rem 2.6rem 2.5rem;
        margin-bottom: 1.7rem;
        border-radius: 30px;
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
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.06), 0 10px 26px rgba(0,0,0,0.18);
    }

    button[data-baseweb="tab"][aria-selected="true"] p {
        color: var(--text-main);
    }

    div[data-testid="stMetric"] {
        padding: 1.15rem 1.15rem 1rem 1.15rem;
        border-radius: 22px;
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

    div[data-testid="stExpander"] {
        border-radius: 16px;
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
    }

    .stButton > button, .stDownloadButton > button {
        min-height: 46px;
        padding: 0.65rem 1.15rem;
        border-radius: 999px;
        border: 1px solid rgba(199, 165, 106, 0.34);
        background:
            linear-gradient(135deg, rgba(199,165,106,0.20), rgba(143,183,209,0.08)),
            rgba(255,255,255,0.04);
        color: var(--text-main);
        font-weight: 800;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.05), 0 12px 30px rgba(0,0,0,0.2);
        transition: all 0.22s ease;
    }

    .stButton > button:hover, .stDownloadButton > button:hover {
        transform: translateY(-2px);
        border-color: rgba(199, 165, 106, 0.52);
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

    .stDataFrame, div[data-testid="stTable"] {
        border-radius: 18px;
        overflow: hidden;
        border: 1px solid rgba(143, 183, 209, 0.12);
        box-shadow: var(--shadow-soft);
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
'''

HERO_HTML = '''
<div class="hero">
    <div class="festival-label">Curated Film Intelligence</div>
    <div class="hero-title">CineStats</div>
    <div class="hero-subtitle">
        A cinematic analytics salon for exploring popular releases, canonical films,
        standout directors, audience response, and category trends through live TMDb data.
    </div>
</div>
'''

st.markdown(APP_CSS, unsafe_allow_html=True)
st.markdown(HERO_HTML, unsafe_allow_html=True)


def tmdb_get(path: str, **params):
    try:
        response = requests.get(
            f"{BASE_URL}{path}",
            params={"api_key": API_KEY, "language": "en-US", **params},
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return {}


@st.cache_data(show_spinner=False)
def get_movies(endpoint: str, pages: int = 10):
    movies = []
    for page in range(1, pages + 1):
        payload = tmdb_get(f"/movie/{endpoint}", page=page)
        movies.extend(payload.get("results", []))
    return movies


@st.cache_data(show_spinner=False)
def get_movie_bundle(movie_id: int):
    return tmdb_get(f"/movie/{movie_id}", append_to_response="credits")


@st.cache_data(show_spinner=False)
def search_movies(query: str):
    payload = tmdb_get("/search/movie", query=query)
    return payload.get("results", [])


@st.cache_data(show_spinner=False)
def get_genre_list():
    payload = tmdb_get("/genre/movie/list")
    genres = payload.get("genres", [])
    return {genre["id"]: genre["name"] for genre in genres}


def build_df(movies, genre_map):
    rows = []
    for movie in movies:
        genres = [genre_map.get(gid, "Unknown") for gid in movie.get("genre_ids", [])]
        rows.append(
            {
                "ID": movie.get("id"),
                "Title": movie.get("title", "N/A"),
                "Release Year": movie.get("release_date", "N/A")[:4] if movie.get("release_date") else "N/A",
                "Rating": movie.get("vote_average", 0.0),
                "Votes": movie.get("vote_count", 0),
                "Popularity": round(movie.get("popularity", 0), 1),
                "Genre": genres[0] if genres else "Unknown",
                "All Genres": ", ".join(genres),
                "Overview": movie.get("overview", ""),
                "Poster": f"{IMAGE_BASE_URL}{movie['poster_path']}" if movie.get("poster_path") else "",
            }
        )
    return pd.DataFrame(rows)


@st.cache_data(show_spinner=False)
def build_director_data(movie_ids):
    director_stats = {}
    for movie_id in movie_ids:
        bundle = get_movie_bundle(movie_id)
        credits = bundle.get("credits", {})
        for person in credits.get("crew", []):
            if person.get("job") != "Director":
                continue

            name = person["name"]
            rating = bundle.get("vote_average", 0)
            revenue = bundle.get("revenue", 0)
            title = bundle.get("title", "Unknown")
            year = bundle.get("release_date", "")[:4]
            photo = f"{IMAGE_BASE_URL}{person.get('profile_path')}" if person.get("profile_path") else ""

            if name not in director_stats:
                director_stats[name] = {
                    "Movies": [],
                    "Ratings": [],
                    "Revenue": [],
                    "Photo": photo,
                }

            director_stats[name]["Movies"].append(f"{title} ({year})")
            director_stats[name]["Ratings"].append(rating)
            director_stats[name]["Revenue"].append(revenue)

    return director_stats


CHART_COLORS = ["#c7a56a", "#8fb7d1", "#6b8194", "#d9c4a0", "#5a6a78", "#b2cadc"]
CONTINUOUS_SCALE = [(0.0, "#213241"), (0.45, "#5d7588"), (1.0, "#c7a56a")]


def curated_chart(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f2eee6", family="Manrope, sans-serif"),
        title=dict(font=dict(size=20, color="#f2eee6"), x=0.0),
        margin=dict(l=20, r=20, t=40, b=20),
        legend_title_text="",
        colorway=CHART_COLORS,
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor="rgba(143, 183, 209, 0.12)",
        zeroline=False,
        showline=False,
        tickfont=dict(color="#aab6c4"),
        title_font=dict(color="#c9dceb"),
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(143, 183, 209, 0.08)",
        zeroline=False,
        showline=False,
        tickfont=dict(color="#aab6c4"),
        title_font=dict(color="#c9dceb"),
    )
    return fig


def render_movie_card(row, icon):
    with st.expander(f"{icon} {row['Title']} ({row['Release Year']}) — {row['Rating']}/10"):
        col1, col2 = st.columns([1, 4])
        with col1:
            if row["Poster"]:
                st.image(row["Poster"], width=115)
        with col2:
            st.markdown(
                f"<span class='gold-text'>Category:</span> {row['All Genres']}",
                unsafe_allow_html=True,
            )
            st.write(f"**Popularity:** {row['Popularity']}")
            st.write(f"**Votes:** {row['Votes']:,}")
            if row["Overview"]:
                st.caption(row["Overview"][:260] + "...")


with st.spinner("Curating the film archive..."):
    popular = get_movies("popular", 10)
    top_rated = get_movies("top_rated", 10)
    genre_map = get_genre_list()

if not popular or not top_rated or not genre_map:
    st.error("Unable to load TMDb data right now. Please check your API key or try again later.")
    st.stop()

df_popular = build_df(popular, genre_map)
df_top = build_df(top_rated, genre_map)

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Overview", "Director Ledger", "Popular Titles", "Top Rated", "Search Archive"]
)

with tab1:
    st.markdown('<div class="section-title">Analytics Overview</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-caption">A curated view of audience ratings, popularity, release eras, and category composition.</div>',
        unsafe_allow_html=True,
    )

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Popular Movies", len(df_popular))
    m2.metric("Top Rated Titles", len(df_top))
    m3.metric("Categories", len(genre_map))
    m4.metric("Avg Top Rating", round(df_top["Rating"].mean(), 2))

    st.markdown("---")

    ch1, ch2 = st.columns(2)
    with ch1:
        st.markdown("### Category Distribution")
        genre_count = df_popular["Genre"].value_counts().reset_index()
        genre_count.columns = ["Category", "Count"]
        fig1 = px.pie(
            genre_count,
            names="Category",
            values="Count",
            hole=0.52,
            color_discrete_sequence=CHART_COLORS,
        )
        fig1.update_traces(
            textfont_color="#f2eee6",
            marker=dict(line=dict(color="rgba(7,16,25,0.85)", width=1.2)),
        )
        st.plotly_chart(curated_chart(fig1), use_container_width=True, theme=None)

    with ch2:
        st.markdown("### Top 10 Rated Films")
        top10 = df_top.sort_values("Rating", ascending=False).head(10)
        fig2 = px.bar(
            top10,
            x="Rating",
            y="Title",
            orientation="h",
            color="Rating",
            color_continuous_scale=CONTINUOUS_SCALE,
            range_x=[0, 10],
        )
        fig2.update_layout(yaxis_title="", xaxis_title="Rating")
        st.plotly_chart(curated_chart(fig2), use_container_width=True, theme=None)

    ch3, ch4 = st.columns(2)
    with ch3:
        st.markdown("### Movies by Release Year")
        year_df = df_top[df_top["Release Year"] != "N/A"].copy()
        year_count = year_df["Release Year"].value_counts().sort_index().reset_index()
        year_count.columns = ["Year", "Count"]
        fig3 = px.line(
            year_count,
            x="Year",
            y="Count",
            markers=True,
            color_discrete_sequence=["#8fb7d1"],
        )
        fig3.update_traces(line=dict(width=3), marker=dict(size=8, color="#c7a56a"))
        st.plotly_chart(curated_chart(fig3), use_container_width=True, theme=None)

    with ch4:
        st.markdown("### Average Rating by Category")
        avg_genre = df_top.groupby("Genre")["Rating"].mean().round(2).reset_index()
        avg_genre.columns = ["Category", "Avg Rating"]
        avg_genre = avg_genre.sort_values("Avg Rating", ascending=False)
        fig4 = px.bar(
            avg_genre,
            x="Category",
            y="Avg Rating",
            color="Avg Rating",
            color_continuous_scale=CONTINUOUS_SCALE,
            range_y=[0, 10],
        )
        fig4.update_layout(xaxis_title="", yaxis_title="Average Rating")
        st.plotly_chart(curated_chart(fig4), use_container_width=True, theme=None)

    st.markdown("### Rating vs Popularity")
    fig5 = px.scatter(
        df_popular,
        x="Popularity",
        y="Rating",
        hover_name="Title",
        color="Genre",
        size="Votes",
        color_discrete_sequence=CHART_COLORS,
    )
    fig5.update_layout(xaxis_title="Popularity", yaxis_title="Rating")
    st.plotly_chart(curated_chart(fig5), use_container_width=True, theme=None)

    st.markdown("---")
    st.markdown("### Full Movie Data Table")
    st.markdown(
        '<div class="section-caption">Filter, sort, and inspect the working dataset.</div>',
        unsafe_allow_html=True,
    )

    tbl1, tbl2, tbl3 = st.columns(3)
    with tbl1:
        tbl_genre = st.multiselect("Filter by Genre", options=sorted(df_popular["Genre"].unique()))
    with tbl2:
        tbl_year = st.multiselect("Filter by Year", options=sorted(df_popular["Release Year"].unique(), reverse=True))
    with tbl3:
        tbl_min_rating = st.slider("Min Rating", 0.0, 10.0, 0.0, 0.1)

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
        height=400,
    )
    st.caption(f"Showing {len(df_table)} movies")

    csv_all = df_table.to_csv(index=False).encode("utf-8")
    st.download_button("Export Table as CSV", csv_all, "cinestats_movies.csv", "text/csv")

with tab2:
    st.markdown('<div class="section-title">Director Ledger</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-caption">A focused study of directors represented in the top-rated selection.</div>',
        unsafe_allow_html=True,
    )

    top50_ids = df_top.sort_values("Rating", ascending=False).head(50)["ID"].tolist()
    with st.spinner("Building the director ledger..."):
        director_data = build_director_data(tuple(top50_ids))

    dir_rows = []
    for name, data in director_data.items():
        avg_rating = round(sum(data["Ratings"]) / len(data["Ratings"]), 2)
        total_revenue = sum(data["Revenue"])
        movie_count = len(data["Movies"])
        best_movie = data["Movies"][data["Ratings"].index(max(data["Ratings"]))]
        dir_rows.append(
            {
                "Director": name,
                "Movies Count": movie_count,
                "Avg Rating": avg_rating,
                "Best Movie": best_movie,
                "Total Revenue": total_revenue,
                "Photo": data["Photo"],
            }
        )

    df_dir = pd.DataFrame(dir_rows).sort_values(["Avg Rating", "Movies Count"], ascending=[False, False])

    d1, d2, d3 = st.columns(3)
    d1.metric("Directors Analyzed", len(df_dir))
    d2.metric("Highest Avg Rating", df_dir["Avg Rating"].max())
    d3.metric("Most Prolific", df_dir.sort_values("Movies Count", ascending=False).iloc[0]["Director"])

    st.markdown("---")

    dc1, dc2 = st.columns(2)
    with dc1:
        st.markdown("### Top 15 Directors by Rating")
        top_dir = df_dir.head(15)
        fig_d1 = px.bar(
            top_dir,
            x="Avg Rating",
            y="Director",
            orientation="h",
            color="Avg Rating",
            color_continuous_scale=CONTINUOUS_SCALE,
            range_x=[0, 10],
        )
        fig_d1.update_layout(yaxis_title="", xaxis_title="Average Rating")
        st.plotly_chart(curated_chart(fig_d1), use_container_width=True, theme=None)

    with dc2:
        st.markdown("### Directors by Number of Films")
        prolific = df_dir.sort_values("Movies Count", ascending=False).head(15)
        fig_d2 = px.bar(
            prolific,
            x="Movies Count",
            y="Director",
            orientation="h",
            color="Movies Count",
            color_continuous_scale=CONTINUOUS_SCALE,
        )
        fig_d2.update_layout(yaxis_title="", xaxis_title="Film Count")
        st.plotly_chart(curated_chart(fig_d2), use_container_width=True, theme=None)

    st.markdown("### Rating vs Total Revenue")
    df_dir_plot = df_dir[df_dir["Total Revenue"] > 0]
    fig_d3 = px.scatter(
        df_dir_plot,
        x="Avg Rating",
        y="Total Revenue",
        hover_name="Director",
        size="Movies Count",
        color="Avg Rating",
        color_continuous_scale=CONTINUOUS_SCALE,
        labels={"Total Revenue": "Total Revenue (USD)"},
    )
    st.plotly_chart(curated_chart(fig_d3), use_container_width=True, theme=None)

    st.markdown("---")
    st.markdown("### Director Data Table")
    st.markdown(
        '<div class="section-caption">Full list of directors sorted by average rating.</div>',
        unsafe_allow_html=True,
    )

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
        height=350,
    )
    st.caption(f"Showing {len(df_dir_tbl)} directors")

    st.markdown("---")
    st.markdown("### Director Detail Search")
    dir_search = st.text_input("Search a director name")
    if dir_search:
        result = df_dir[df_dir["Director"].str.contains(dir_search, case=False, na=False)]
        if not result.empty:
            for _, row in result.iterrows():
                with st.expander(f"🎬 {row['Director']} — {row['Avg Rating']} avg"):
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
    st.download_button("Export Director Data as CSV", csv_dir, "cinestats_directors.csv", "text/csv")

with tab3:
    st.markdown('<div class="section-title">Popular Titles</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-caption">A living shortlist of titles currently drawing the widest audience attention.</div>',
        unsafe_allow_html=True,
    )

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
        render_movie_card(row, "🎬")

with tab4:
    st.markdown('<div class="section-title">Top Rated Canon</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-caption">A sortable view into the highest-rated films surfaced from TMDb.</div>',
        unsafe_allow_html=True,
    )

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

    st.markdown("### Table View")
    st.dataframe(
        df_t[["Title", "Release Year", "Genre", "All Genres", "Rating", "Votes", "Popularity"]],
        use_container_width=True,
        height=350,
    )
    st.caption(f"{len(df_t)} movies in this view")

    st.markdown("---")

    for _, row in df_t.head(20).iterrows():
        render_movie_card(row, "🏆")

with tab5:
    st.markdown('<div class="section-title">Search Archive</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-caption">Search a film title and review its poster, rating, votes, and synopsis.</div>',
        unsafe_allow_html=True,
    )

    query = st.text_input(
        "Enter a movie title",
        placeholder="e.g. Inception, Parasite, La La Land...",
    )

    if query:
        with st.spinner("Searching the archive..."):
            results = search_movies(query)

        if results:
            df_s = build_df(results, genre_map)
            st.success(f"Found {len(df_s)} results for '{query}'")

            st.markdown("### Search Results Table")
            st.dataframe(
                df_s[["Title", "Release Year", "Genre", "Rating", "Votes"]],
                use_container_width=True,
                height=300,
            )
            st.markdown("---")

            for _, row in df_s.head(10).iterrows():
                render_movie_card(row, "🎬")
        else:
            st.warning("No results found. Try another movie title.")

st.markdown("---")
csv = df_top.to_csv(index=False).encode("utf-8")
st.download_button(
    "Export Top Rated Movies as CSV",
    csv,
    "cinestats_top_rated.csv",
    "text/csv",
    use_container_width=True,
)
