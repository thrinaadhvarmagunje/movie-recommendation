import streamlit as st
import pickle
import requests
import os
import pandas as pd

# ---------------------------------------------
# GOOGLE DRIVE DOWNLOAD FOR similarity.pkl
# ---------------------------------------------
def download_similarity():
    url = "https://drive.google.com/uc?export=download&id=1oV3po_Vf-Aes_NF1jAzunESTHZ9_32oX"

    if not os.path.exists("similarity.pkl"):
        st.write("Downloading similarity data... Please wait.")
        r = requests.get(url)
        with open("similarity.pkl", "wb") as f:
            f.write(r.content)
        st.write("Download complete!")

download_similarity()

# Load similarity file
with open("similarity.pkl", "rb") as f:
    similarity = pickle.load(f)

# Load movies dict
movies_dict = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)


# ---------------------------------------------
# FETCH MOVIE POSTER FROM OMDb API
# ---------------------------------------------
API_KEY = "ccd9f1f8"   # your OMDb API key

def fetch_poster(movie_title):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={API_KEY}"
    data = requests.get(url).json()

    if data.get("Response") == "True":
        return data.get("Poster")
    else:
        return "https://via.placeholder.com/300x450?text=No+Image"


# ---------------------------------------------
# RECOMMENDATION FUNCTION
# ---------------------------------------------
def recommend(movie):
    idx = movies[movies['title'] == movie].index[0]
    distances = similarity[idx]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommended_titles = []
    recommended_posters = []

    for i in movie_list:
        movie_title = movies.iloc[i[0]].title
        recommended_titles.append(movie_title)
        recommended_posters.append(fetch_poster(movie_title))

    return recommended_titles, recommended_posters


# ---------------------------------------------
# PAGE STYLING
# ---------------------------------------------
st.markdown("""
    <style>
        body {
            background-color: #000000;
        }
        .title {
            font-size: 50px;
            font-weight: 800;
            color: red;
            text-align: center;
            padding-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🎬 Movie Recommender</div>', unsafe_allow_html=True)


# ---------------------------------------------
# UI
# ---------------------------------------------
selected_movie = st.selectbox(
    "Search or select a movie",
    movies['title'].values
)

if st.button("Recommend"):
    with st.spinner("Finding similar movies..."):
        names, posters = recommend(selected_movie)

    st.subheader("Recommended Movies")
    cols = st.columns(5)

    for i in range(10):
        with cols[i % 5]:
            st.image(posters[i], use_column_width=True)
            st.write(names[i])
