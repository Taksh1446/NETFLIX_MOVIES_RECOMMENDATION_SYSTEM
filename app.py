import streamlit as st
import pandas as pd
import pickle
import requests
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Netflix Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# ---------------- NETFLIX STYLE UI ----------------
st.markdown("""
<style>

.stApp{
background-color:#0f0f0f;
color:white;
}

h1{
color:#E50914;
text-align:center;
}

.stButton>button{
background-color:#E50914;
color:white;
border-radius:10px;
height:3em;
width:220px;
font-size:18px;
}

img:hover{
transform: scale(1.08);
transition: 0.3s;
}

footer{
visibility:hidden;
}

</style>
""", unsafe_allow_html=True)

# ---------------- FILE PATH ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
movies_path = os.path.join(BASE_DIR,"movies_dict.pkl")
similarity_path = os.path.join(BASE_DIR,"similarity.pkl")

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():

    if not os.path.exists(movies_path):
        st.error("movies_dict.pkl file not found")
        st.stop()

    if not os.path.exists(similarity_path):
        st.error("similarity.pkl file not found")
        st.stop()

    with open(movies_path,'rb') as f:
        movies_dict = pickle.load(f)

    with open(similarity_path,'rb') as f:
        similarity = pickle.load(f)

    return pd.DataFrame(movies_dict), similarity


data, similarity = load_model()

# ---------------- TMDB API ----------------
API_KEY = "7a58541684c01a029cd8a324fef5ca4e"

def fetch_movie_details(movie_id):

    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        response = requests.get(url, timeout=5)
        movie = response.json()

        poster = "https://via.placeholder.com/500x750?text=No+Poster"

        if movie.get("poster_path"):
            poster = "https://image.tmdb.org/t/p/w500/" + movie["poster_path"]

        rating = movie.get("vote_average","N/A")
        overview = movie.get("overview","No overview available")
        release = movie.get("release_date","Unknown")

        return poster,rating,overview,release

    except:
        return "https://via.placeholder.com/500x750?text=No+Poster","N/A","No overview","Unknown"


# ---------------- RECOMMEND FUNCTION ----------------
def recommend(movie):

    recommended_movies=[]
    recommended_posters=[]
    ratings=[]
    overviews=[]
    releases=[]

    movie_match = data[data['title']==movie]

    if movie_match.empty:
        return [],[],[],[],[]

    movie_index = movie_match.index[0]
    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x:x[1]
    )[1:6]

    for i in movie_list:

        movie_id = data.iloc[i[0]].movie_id
        title = data.iloc[i[0]].title

        poster,rating,overview,release = fetch_movie_details(movie_id)

        recommended_movies.append(title)
        recommended_posters.append(poster)
        ratings.append(rating)
        overviews.append(overview)
        releases.append(release)

    return recommended_movies,recommended_posters,ratings,overviews,releases


# ---------------- SIDEBAR ----------------
st.sidebar.title("🎬 About Project")

st.sidebar.info("""
Netflix Movie Recommendation System

Machine Learning Model:
Content Based Filtering

Dataset:
TMDB Movie Dataset

Built Using:
Python, Pandas, Streamlit
""")

# ---------------- HEADER ----------------
st.title("🎬 Netflix Movie Recommendation System")

st.markdown(
"<center>Discover movies similar to your favorite ones 🍿</center>",
unsafe_allow_html=True
)

st.write("")

# ---------------- TRENDING MOVIES ----------------
st.subheader("🔥 Trending Movies")

trending = data.sample(5)
cols = st.columns(5)

for i,col in enumerate(cols):

    movie_id = trending.iloc[i].movie_id
    poster,rating,overview,release = fetch_movie_details(movie_id)

    with col:
        st.image(poster, use_container_width=True)
        st.caption(trending.iloc[i].title)

st.write("---")

# ---------------- SEARCH BAR ----------------
search_movie = st.text_input("🔎 Search for a movie")

if search_movie:
    filtered_movies = data[data['title'].str.contains(search_movie, case=False, na=False)]
else:
    filtered_movies = data

# ---------------- SELECT MOVIE ----------------
selected_movie = st.selectbox(
"Choose a movie",
filtered_movies['title'].values
)

# ---------------- RECOMMEND BUTTON ----------------
if st.button("Recommend Movies 🍿"):

    with st.spinner("Finding best movies for you..."):

        names,posters,ratings,overviews,releases = recommend(selected_movie)

        if len(names) == 0:
            st.warning("Movie not found in dataset.")
            st.stop()

        columns = st.columns(5)

        for i,col in enumerate(columns):

            with col:

                st.image(posters[i], use_container_width=True)

                st.markdown(f"**{names[i]}**")

                st.write("⭐ Rating:",ratings[i])
                st.write("📅 Release:",releases[i])

                with st.expander("📖 Overview"):
                    st.write(overviews[i])


# ---------------- FOOTER ----------------
st.markdown("---")

st.markdown(
"<center>Built with ❤️ using Streamlit | Movie Recommendation ML Project</center>",
unsafe_allow_html=True
)
