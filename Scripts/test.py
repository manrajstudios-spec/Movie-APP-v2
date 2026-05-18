# %%
import requests
import time
import pandas as pd
session = requests.Session()

df = pd.read_csv("/home/manraj_studios/Python/Movie-APP-v2/Data/movie_dataset.csv")
import os
from dotenv import load_dotenv 
load_dotenv() 
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
# %%
def get_movie_poster(movie_id):

    try:

        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"

        response = session.get(
            url,
            timeout=10
        )

        data = response.json()

        poster_path = data.get("poster_path")

        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"

    except Exception as e:

        print(f"Movie ID {movie_id}: {e}")

    return None

# %%

for i, movie in df.iterrows():

    try:

        df.loc[i, "poster_path"] = get_movie_poster(movie["id"])

        print(f"Done {i}")


    except Exception as e:

        print(e)
# %%
df.to_csv(
    "/home/manraj_studios/Python/Movie-APP-v2/Data/movie_dataset.csv",
    index=False
)
# %%
df.poster_path[0]
# %%
