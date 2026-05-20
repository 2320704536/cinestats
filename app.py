import pandas as pd
import plotly.express as px
import requests
import streamlit as st


st.set_page_config(
    page_title="CineStats — Film Festival Analytics",
    page_icon="🎬",
    layout="wide",
)


API_KEY = st.secrets.get("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w200"
REQUEST_TIMEOUT = 20


if not API_KEY:
    st.error("TMDb API key is missing. Add `TMDB_API_KEY` to your Streamlit secrets.")
    st.stop()


st.markdown(
    """
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
