# %%
import pandas as pd
import numpy as np
from Data_Loader import return_dataset
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# %%
df = pd.read_csv("/home/manraj_studios/Python/Movie-APP-v2/Data/movie_dataset")

# %%
df.genres

# %%
def clean_genres(df:pd.DataFrame):
    df.genres = df['genres'].str.removeprefix('[{"')
    df.genres = df['genres'].str.removesuffix('"}]')
    df.genres = df['genres'].str.split(',')

    def genre(lst):
        genres = []
        for i,g in enumerate(lst):
            if i % 2 == 0:continue
            genres.append(g)

        return genres
    
    df['genres'] =df['genres'].apply(genre)

    def genre_set(lst):
        genres = []

        for g in lst:
            g = g.strip()
            g = g.replace('"name":','')
            g = g.replace('"','')
            g = g.replace('"','')
            g = g.replace('}','')
            g = g.strip()
            genres.append(g)

        return genres
    df['genres'] =df['genres'].apply(genre_set)

    return df.genres

# %%
df.genres = clean_genres(df)

# %%
# %% 
df
# %%
