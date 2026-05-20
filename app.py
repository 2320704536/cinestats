import html

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


APP_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Cormorant+Garamond:wght@500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
        --bg-main: #080c11;
        --bg-deep: #111820;
        --bg-panel: rgba(15, 24, 34, 0.88);
        --bg-panel-soft: rgba(19, 29, 41, 0.72);
        --bg-warm: rgba(72, 47, 28, 0.18);
        --bg-cool: rgba(52, 79, 102, 0.16);
        --bg-olive: rgba(72, 97, 84, 0.14);
        --line-soft: rgba(160, 180, 199, 0.18);
        --line-bold: rgba(203, 169, 109, 0.35);
        --text-main: #f4efe6;
        --text-soft: #b5c0cd;
        --text-faint: rgba(181, 192, 205, 0.68);
        --gold: #cba96d;
        --gold-soft: #dfc596;
        --silver: #91aec5;
        --ember: #b97353;
        --moss: #6f8c79;
        --plum: #7e6f8f;
        --shadow-deep: 0 32px 80px rgba(0, 0, 0, 0.42);
        --shadow-soft: 0 18px 38px rgba(0, 0, 0, 0.24);
    }

    html, body, [class*="css"] {
        font-family: "Manrope", sans-serif;
    }

    .stApp {
        color: var(--text-main);
        background:
            radial-gradient(circle at 18% 12%, rgba(203, 169, 109, 0.08), transparent 20%),
            radial-gradient(circle at 84% 22%, rgba(145, 174, 197, 0.08), transparent 24%),
            radial-gradient(circle at 52% 86%, rgba(111, 140, 121, 0.08), transparent 26%),
            linear-gradient(140deg, #040608 0%, #090d12 25%, #0f151d 60%, #131b24 100%);
        background-attachment: fixed;
        position: relative;
    }

    .stApp::before {
        content: "";
        position: fixed;
        inset: 14px;
        border: 1px solid rgba(203, 169, 109, 0.12);
        pointer-events: none;
        z-index: 0;
    }

    .stApp::after {
        content: "";
        position: fixed;
        inset: 0;
        background:
            repeating-linear-gradient(
                180deg,
                rgba(255, 255, 255, 0.012) 0px,
                rgba(255, 255, 255, 0.012) 1px,
                transparent 1px,
                transparent 4px
            );
        mix-blend-mode: soft-light;
        opacity: 0.3;
        pointer-events: none;
        z-index: 0;
    }

    .block-container {
        position: relative;
        z-index: 1;
        max-width: 1260px;
        padding-top: 1.9rem;
