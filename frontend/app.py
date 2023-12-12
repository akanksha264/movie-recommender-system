import streamlit as st
import pickle
import os
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = 'https://api.themoviedb.org/3/movie/{}?api_key=df20ee8aeb3b1bf393731df68c0fd1b2&language=en-US'
    response = requests.get(url.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie) :
    # Retrieve the index of given movie
    movie_index = movies[movies['title'].str.lower() == movie.lower()].index[0]

    # Find similarity vector of the movie
    distances = similarity[movie_index]

    # Convert the vector to indexed vector
    indexed_distances = list(enumerate(distances))

    # Sort in reverse based on similarity value
    sorted_distances = sorted(indexed_distances, reverse=True, key=lambda x: x[1])

    # Find 5 closest movies
    top_five = sorted_distances[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in top_five:
        recommended_movies.append(movies.iloc[i[0]].title)
        # Fetch poster from API
        recommended_movies_posters.append(fetch_poster(movies.iloc[i[0]].movie_id))

    return recommended_movies,recommended_movies_posters


# Get the current working directory
current_directory = os.getcwd()

# Load list of movies
movies_list = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_list)

# Load similarity matrix
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("Movie Recommender System")

option = st.selectbox(
    'Select a movie',
    movies['title'].values)

if st.button('Recommend'):
    names,posters = recommend(option)
    num_columns = len(names)

    # Create columns dynamically
    columns = st.columns(num_columns)

    # Populate columns with names as headers and posters as data
    for col, (name, poster) in zip(columns, zip(names, posters)):
        with col:
            # Display the name with line breaks
            st.image(poster)
            st.markdown(f"**{name}**", unsafe_allow_html=True)
