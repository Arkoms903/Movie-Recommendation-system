import streamlit as st
import pickle
import requests
import pandas as pd

st.title('Movie Recommendation System')

@st.cache_data
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=67b283c85107f26f922daec2af554bd0"
    data = requests.get(url).json()
    poster_path = data.get("poster_path")
    
    if poster_path:
        return "https://image.tmdb.org/t/p/w342" + poster_path
    else:
        return "https://via.placeholder.com/342x500?text=No+Image"

@st.cache_data
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    
    return recommended_movies, recommended_posters

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

selected_movie_name = st.selectbox("Select a movie", movies['title'].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.text(names[i])
            st.image(posters[i])
