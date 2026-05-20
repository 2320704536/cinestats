
    csv_dir = df_dir.drop(columns=["Photo"]).to_csv(index=False).encode("utf-8")
    st.download_button(
        "Export Director Data as CSV",
        csv_dir,
        "cinestats_directors.csv",
        "text/csv",
    )


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
