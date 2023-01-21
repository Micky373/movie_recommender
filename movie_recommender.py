import pickle # For model loading
import streamlit as st # For the UI
import requests # For http requests
import pandas as pd
# For string vector conversion and similarity calculation
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Loading the dataset and similarity vectors

movies_df = pd.read_csv('data/movies_df.csv')

cv = CountVectorizer(max_features=5000,
                    stop_words='english')
vector = cv.fit_transform(movies_df['tags']).toarray()
similarity = cosine_similarity(vector)

# Creating movie titles array

movie_titles = list(movies_df['title'].values)

# A function for api request of poster images

def fetch_poster(movie_id):
    
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".\
                            format(movie_id)
    try:
        response = requests.get(url)
        response = response.json()
        image_api = "https://image.tmdb.org/t/p/w500/"
        poster_path = response['poster_path']
    except:
        return "The movie you passed doesn't exist"
    
    return image_api + poster_path


# Recommender system that returns movie names and their poster path

def recommend(movie):
    
    try:

        index_ = movies_df[movies_df['title'] == movie].index[0]
    
        similaity_vec = list(enumerate(similarity[index_]))
        similarity_vec = sorted(similaity_vec,reverse=True,key = lambda x:x[1])

        recommended_movies = []
        poster_pathes = []
        
        for i in range(1,11):
            title = movies_df.loc[similarity_vec[i][0]]['title']
            movie_id = movies_df.loc[similarity_vec[i][0]]['movie_id']
            recommended_movies.append(title)
            poster_pathes.append(fetch_poster(movie_id))
            
    except:
        recommended_movies = []
        poster_pathes = []    
    
    
    return recommended_movies,poster_pathes

# Creating a page title
st.set_page_config(
    page_title = 'Movie Recommendation'
)

# Making a title for our UI
st.header('Movie Recommender System')

# Creating a selectbox 

selected_movies = st.selectbox(
    'Type or select a movie from the dropdown below',
    movie_titles
)

if st.button('Show recommendations'):

    # Getting the movie names and their poster images

    movie_names,movie_posters = recommend(selected_movies)

    if len(movie_names) > 0  and len(movie_posters) > 0:
        # Creating a five column display for easy look of our UI

        col1,col2,col3,col4,col5 = st.columns(5)

        column_names = [col1,col2,col3,col4,col5]

        for i in range(10):
            
            if i >= 5:
                column_index = i - 5
            
            else:
                column_index = i
            
            # Displaying all the images and movie titles

            with column_names[column_index]:
                st.text(movie_names[i])
                st.image(movie_posters[i])
    
    else:
        st.header('No related movies here')

        
