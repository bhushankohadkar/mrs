import streamlit as st
import pickle
import pandas as pd
import requests
from PIL.Image import Image

movies_list = pickle.load(open('movie_dict.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))


movies = pd.DataFrame(movies_list)


st.title("Movie Recommendation system")   #title
select_movie_name = st.selectbox('Select Movie name',movies['title'].values)

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=84d4ec28fa85fa521aa54fe07c45f31d&language=en-US'.format(movie_id))
    data= response.json()
    #st.text(data)
    #st.text('https://api.themoviedb.org/3/movie/{}?api_key=84d4ec28fa85fa521aa54fe07c45f31d&language=en-US'.format(movie_id))
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_poster.append((fetch_poster(movie_id)))
    return recommended_movies, recommended_movies_poster


# create button
if st.button('Recommend'):
    names, posters = recommend(select_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])



