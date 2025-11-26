import pickle
import streamlit as st
import pandas as pd
import requests
import os

# ============================================================
#           GOOGLE DRIVE DOWNLOAD (LARGE FILE FIX)
# ============================================================
def download_similarity():
    file_id = "1oV3po_Vf-Aes_NF1jAzunESTHZ9_32oX"
    destination = "similarity.pkl"

    if os.path.exists(destination):
        return  # already downloaded

    st.write("Downloading similarity data from Google Drive...")

    URL = "https://drive.google.com/uc?export=download"
    session = requests.Session()

    # First request
    response = session.get(URL, params={"id": file_id}, stream=True)

    # Check for confirm token
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith("download_warning"):
                return value
        return None

    token = get_confirm_token(response)

    if token:
        params = {"id": file_id, "confirm": token}
        response = session.get(URL, params=params, stream=True)

    # Save the file
    with open(destination, "wb") as f:
        for chunk in response.iter_content(32768):
            if chunk:
                f.write(chunk)

    st.success("Download complete!")

# Download similarity file
download_similarity()


# ============================================================
#                  NETFLIX STYLE UI THEMING
# ============================================================
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">

<style>
* { font-family: 'Poppins', sans-serif; }

.stApp { background-color: #141414; }

h1, h2, h3 {
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
#                FIXED OMDb POSTER FETCHING
# ============================================================
API_KEY = "ccd9f1f8"

def fetch_poster(movie_title):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={API_KEY}"
    data = requests.get(url).json()

    if data.get("Response") == "True" and data.get("Poster") != "N/A":
        return data["Poster"]

    return "https://via.placeholder.com/300x450/000000/FFFFFF?text=No+Poster"


# ============================================================
#                     RECOMMENDATION LOGIC
# ============================================================
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        title = movies.iloc[i[0]].title
        recommended_movies.append(title)
        recommended_posters.append(fetch_poster(title))

    return recommended_movies, recommended_posters


# ============================================================
#                        LOAD FILES
# ============================================================
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

with open("similarity.pkl", "rb") as f:
    similarity = pickle.load(f)


# ============================================================
#                          MAIN UI
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
