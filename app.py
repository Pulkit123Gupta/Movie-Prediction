import streamlit as st
import pickle
import pandas as pd
import requests

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Movie Recommendation",
    page_icon="🎬",
    layout="wide"
)


# -------------------------------
# Helper Functions
# -------------------------------
def fetch_poster(movie_id):
    """Fetch movie poster from TMDB API."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(url)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    """Recommend 5 movies similar to the selected one."""
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(
        list(enumerate(distance)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []
    recommended_links = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
        recommended_links.append(f"https://www.themoviedb.org/movie/{movie_id}")

    return recommended_movies, recommended_posters, recommended_links


# -------------------------------
# Load Data
# -------------------------------
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.title("⚙️ Settings")
st.sidebar.write("Customize your recommendation experience.")
st.sidebar.markdown("---")
st.sidebar.info("Built with ❤️ using Streamlit and TMDB API")

# -------------------------------
# Main Title
# -------------------------------
st.title("🎬 Movie Recommendation System")
st.markdown(
    "Get **personalized movie recommendations** based on your favorite film. "
    "Our system uses content-based filtering to find the most similar movies for you!"
)

# -------------------------------
# Movie Selector
# -------------------------------
option = st.selectbox(
    "🔎 Select a movie you like:",
    movies['title'].values
)

if st.button("Recommend 🎥"):
    names, posters, links = recommend(option)

    st.markdown("### ✨ Recommended Movies for You:")
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            # Clickable poster
            col.markdown(
                f"<a href='{links[idx]}' target='_blank'>"
                f"<img src='{posters[idx]}' width='100%'></a>",
                unsafe_allow_html=True
            )
            # Clickable title
            col.markdown(
                f"<a href='{links[idx]}' target='_blank'><b>{names[idx]}</b></a>",
                unsafe_allow_html=True
            )
