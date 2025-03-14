import pickle
import requests
import streamlit as st
import pandas as pd
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list=sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies=[]
    for i in movie_list:
                recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies


st.title('Movie Recommender System')
movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))
selected_movie = st.selectbox(
    "choose a movie which you have seen",
    movies['title'].values
    
)

if st.button('Show Recommendation'):
    names=recommend(selected_movie)
    st.text("YOU MIGHT ALSO LIKE THE FOLLOWIG")
    col1, col2, col3,col4,col5= st.columns(5)
    with col1:
           st.text(names[0])
    with col2:
           st.text(names[1])
    with col3:
           st.text(names[2])
    with col4:
           st.text(names[3])
    with col5:
           st.text(names[4])   