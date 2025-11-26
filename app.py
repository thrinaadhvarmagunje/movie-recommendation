import streamlit as st
import pandas as pd
import numpy as np
import pickle
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ============================================================
#                  NETFLIX STYLE THEME
# ============================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    * { font-family: 'Poppins', sans-serif; }

    .stApp {
        background-color: #141414;
    }

    h1, h3 {
        color: #E50914 !important;
        font-weight: 700 !important;
        text-align: center !important;
    }

    label, .css-1p3n8nr {
        color: #ffffff !important;
        font-size: 18px !important;
        font-weight: 600;
    }

    .stSelectbox div {
        background-color: #2b2b2b !important;
        color: white !important;
        border-radius: 8px;
    }

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

    .movie-title {
        color: #ffffff;
        background-color: #E50914;
        padding: 6px;
        text-align: center;
        margin-top: 8px;
        border-radius: 6px;
        font-weight: 600;
    }

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
#                   LOAD MOVIES DATA
# ============================================================
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)


# ============================================================
#            BUILD SIMILARITY MATRIX INSIDE STREAMLIT
# ============================================================
@st.cache_resource(show_spinner=True)
def compute_similarity():
    cv = CountVectorizer(max_features=5000, stop_words='english')

    # Convert tags to matrix
    vectors = cv.fit_transform(movies['tags']).toarray()

    # Compute similarity
    similarity_matrix = cosine_similarity(vectors)

    return similarity_matrix

similarity = compute_similarity()


# ============================================================
#                   OMDb POSTER FETCH
# ============================================================
API_KEY = "ccd9f1f8"

def fetch_poster(movie_title):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={API_KEY}"
    data = requests.get(url).json()
    if data.get("Poster") and data.get("Poster") != "N/A":
        return data["Poster"]
    return "https://via.placeholder.com/300x450/000000/FFFFFF?text=No+Image"


# ============================================================
#                 RECOMMENDATION FUNCTION
# ============================================================
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]

    movie_list = sorted(
        list(enumerate(distances)),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    recommended_titles = []
    recommended_posters = []

    for i in movie_list:
        title = movies.iloc[i[0]].title
        recommended_titles.append(title)
        recommended_posters.append(fetch_poster(title))

    return recommended_titles, recommended_posters


# ============================================================
#                         UI
# ============================================================
st.title("🎬 Netflix-Style Movie Recommender")

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
            st.image(posters[i], use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="movie-title">{names[i]}</div>', unsafe_allow_html=True)
