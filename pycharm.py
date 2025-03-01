import pandas as pd
import streamlit as st
import pickle
import requests

# Define the function to fetch poster using TMDb API
def fetch_poster(movie_id):
    # Replace with your RapidAPI key
    api_key = "53a9007d27mshc9e0cd0c8629b72p1a69a1jsnf4b4330878e7"

    # Correct API URL for fetching images
    url = f'https://the-movie-database.p.rapidapi.com/3/movie/{movie_id}/images'

    # Set up the headers with your RapidAPI key
    headers = {
        'X-RapidAPI-Key': api_key,
        'X-RapidAPI-Host': 'the-movie-database.p.rapidapi.com'
    }

    try:
        # Make the request to the API
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to fetch data from the API. Status code: {response.status_code}")
            return "https://via.placeholder.com/500x750?text=Error+Fetching+Poster"

        # Parse the response as JSON
        data = response.json()

        # Check if the 'posters' key exists and has images
        if 'posters' in data and len(data['posters']) > 0:
            poster_path = data['posters'][0].get('file_path', None)
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
            else:
                return "https://via.placeholder.com/500x750?text=No+Poster+Available"
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster+Available"

    except requests.exceptions.RequestException as e:
        print(f"Error during the API request: {e}")
        return "https://via.placeholder.com/500x750?text=Error+Fetching+Poster"


# Function to fetch movie type info from IMDb using their API
def fetch_movie_info_imdb():
    url = "https://imdb236.p.rapidapi.com/imdb/types"

    # Headers for IMDb API request
    headers = {
        "x-rapidapi-key": "53a9007d27mshc9e0cd0c8629b72p1a69a1jsnf4b4330878e7",
        "x-rapidapi-host": "imdb236.p.rapidapi.com"
    }

    try:
        # Make the request to the IMDb API
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to fetch data from IMDb API. Status code: {response.status_code}")
            return None

        # Parse the response as JSON
        data = response.json()

        # Return the data for further use (just print it here for debugging)
        return data

    except requests.exceptions.RequestException as e:
        print(f"Error during IMDb API request: {e}")
        return None


# Load data
# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))


# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommend_movies_poster= []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_movies_poster.append(fetch_poster(movie_id))
    return recommend_movies ,recommend_movies_poster

# Streamlit app
st.title('Movie Recommender System')

# Dropdown for movie selection
selection_movie_name = st.selectbox(
    'Select a movie for recommendations:',
    movies['title'].values
)

# Button to trigger recommendation
if st.button('Recommend'):
    names,poster = recommend(selection_movie_name)
    col1, col2,col3,col4,col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(poster[0])
    with col2:
         st.text(names[1])
         st.image(poster[1])
    with col3:
         st.text(names[2])
         st.image(poster[2])
    with col4:
         st.text(names[3])
         st.image(poster[3])
    with col5:
         st.text(names[4])
         st.image(poster[4])


