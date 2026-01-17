import streamlit as st
import pickle
import pandas as pd
import requests

API_KEY = st.secrets["TMDB_API_KEY"]

movies_list=pd.DataFrame(pickle.load(open('movies.pkl','rb')))
movies=movies_list['title'].values
similarity=pickle.load(open('similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    response=requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US%22')
    data=response.json()
    return "https://image.tmdb.org/t/p/w500"+data['poster_path']



def recommend(movie):
  movie_index=movies_list[movies_list['title']==movie].index[0]
  distances=similarity[movie_index]
  movie_names=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
  recommended_movies=[]
  recommended_movies_poster=[]
  for j in movie_names:
      recommended_movies.append(movies_list.iloc[j[0]].title)
      recommended_movies_poster.append(fetch_poster(movies_list.iloc[j[0]].movie_id))
  return recommended_movies,recommended_movies_poster


st.title("Movie Recommender System")



option=st.selectbox("Select the movie name movie",movies)
if st.button("Recommend"):
    names,posters=recommend(option)
    cols = st.columns(5)

    for idx, col in enumerate(cols):
        with col:
            st.image(posters[idx], use_container_width=True)
            st.caption(names[idx])
