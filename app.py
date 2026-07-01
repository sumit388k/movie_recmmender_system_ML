
import pickle
import streamlit as st
import requests

# TMDB API Key
API_KEY = "219c5f9907b1e5bb95c74c7a2de256b5"


# Fetch Poster
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

        response = requests.get(url, timeout=10)
        data = response.json()

        poster_path = data.get("poster_path")

        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path

        return None

    except:
        return None


# Recommend Movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[movie_index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_names = []
    recommended_posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]]['movie_id']

        recommended_names.append(
            movies.iloc[i[0]]['title']
        )

        recommended_posters.append(
            fetch_poster(movie_id)
        )

    return recommended_names, recommended_posters


# Load Files
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# UI
st.set_page_config(page_title="Movie Recommender")

st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox(
    "Select a Movie",
    movies['title'].values
)

if st.button("Show Recommendation"):

    names, posters = recommend(selected_movie)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.write(names[i])

            if posters[i]:
                st.image(posters[i])
            else:
                st.write("Poster Not Available")
