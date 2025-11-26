import pickle
import streamlit as st
import pandas as pd
import requests

# ============================================================
#                  NETFLIX STYLE UI THEMING
# ============================================================
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">

<style>
* {
    font-family: 'Poppins', sans-serif;
}

/* APP BACKGROUND */
.stApp {
    background-color: #141414;
}

/* TITLE */
h1, h2, h3 {
    color: #E50914 !important;
    font-weight: 700 !important;
    text-align: center !important;
}

/* SELECTBOX LABEL */
.css-1p3n8nr, label {
    color: #ffffff !important;
    font-size: 18px !important;
    font-weight: 600;
}

/* SELECTBOX DROPDOWN */
.stSelectbox div {
    background-color: #2b2b2b !important;
    color: white !important;
    border-radius: 8px;
}

/* BUTTON */
.stButton button {
    background-color: #E50914 !important;
    color: white !important;
    border-radius: 8px;
    padding: 10px 25px;
    font-size: 18px;
    border: none;
    font-weight: 600;
    transition: 0.3s;
}

.stButton button:hover {
    background-color: #b20710 !important;
    transform: scale(1.03);
}

/* MOVIE TITLE UNDER POSTER */
.movie-title {
    color: #ffffff;
    background-color: #E50914;
    padding: 6px;
    text-align: center;
    margin-top: 8px;
    border-radius: 6px;
    font-weight: 600;
}

/* POSTER HOVER EFFECT */
.poster-container img {
    border-radius: 10px;
    transition: 0.3s ease-in-out;
    border: 2px solid transparent;
}

.poster-container img:hover {
    transform: scale(1.08);
    border: 2px solid #E50914;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
#                  OMDb POSTER DOWNLOAD
# ============================================================
API_KEY = "ccd9f1f8"  # your OMDb API Key

def fetch_poster(movie_title):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={API_KEY}"
    data = requests.get(url).json()
    return data.get("Poster", "")

# ============================================================
#                     RECOMMENDATION LOGIC
# ============================================================
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)),
                        reverse=True,
                        key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        title = movies.iloc[i[0]].title
        recommended_movies.append(title)
        recommended_posters.append(fetch_poster(title))

    return recommended_movies, recommended_posters

# ============================================================
#                           MAIN UI
# ============================================================
st.title("🎬 Movie Recommender")

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

selected_movie = st.selectbox(
    "Choose a movie you watched:",
    movies['title'].values
)

if st.button("Show Recommendation"):
    names, posters = recommend(selected_movie)

    st.markdown("<h3>🔥 Recommended For You</h3>", unsafe_allow_html=True)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.markdown('<div class="poster-container">', unsafe_allow_html=True)
            st.image(posters[i])
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="movie-title">{names[i]}</div>', unsafe_allow_html=True)
