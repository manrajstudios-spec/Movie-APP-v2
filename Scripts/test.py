# %%
import pandas as pd
import numpy as np
import json
import ast
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# %%
df = pd.read_csv("/home/manraj_studios/Python/Movie-APP-v2/Data/movie_dataset")

# %%
df['production_countries'] = df['production_countries'].apply(lambda x : ast.literal_eval(x))
df['production_countries'] = df['production_countries'].apply(lambda x :[g['name'].strip() for g in x if 'name' in g])

df['genres'] = df['genres'].apply(lambda x:ast.literal_eval(x))
df['genres'] = df['genres'].apply(lambda x:[g['name'].strip() for g in x if 'name' in g])

df['production_companies'] = df['production_companies'].apply(lambda x : ast.literal_eval(x))
df['production_companies'] = df['production_companies'].apply(lambda x :[g['name'].strip() for g in x if 'name' in g])

df['spoken_languages'] = df['spoken_languages'].apply(lambda x : ast.literal_eval(x))
df['spoken_languages'] = df['spoken_languages'].apply(lambda x :[g['name'].strip() for g in x if 'name' in g])

rating = df['vote_average']
df = df.drop(columns=['vote_average'])
df['rating'] = rating

df['keywords'] = df['keywords'].apply(lambda x : ast.literal_eval(x))
df['keywords'] = df['keywords'].apply(lambda x :[g['name'].strip() for g in x if 'name' in g])


# %%
df['genre_text'] = df['genres'].apply(lambda x : ",".join(g for g in x))
df['keywords_text'] = df['keywords'].apply(lambda x : ",".join(k for k in x))        

# %%
df['story_genre'] = df['overview'] + " "+ "Genres: " + df['genre_text'] + " " + "Key Words: " + df['keywords_text']

# %%
pre = df[df['genres'].apply(
    lambda x: 'Action' in x
)].head(10)
# %%
model = SentenceTransformer("all-MiniLM-L6-v2")

# %%
story_score = model.encode(df['story_genre'].to_list())

# %%
watched_story_score = model.encode(pre['story_genre'].to_list())

# %%
df = df[~df['id'].isin(pre['id'])].copy()

# %%
similarity = cosine_similarity(watched_story_score,story_score)

# %%
similarity = similarity.mean(axis=0)

# %%
similarity_indices = np.argsort(similarity)[::-1][:10]

# %%
similarity.mean(axis=0)

# %%
# %%
df.index
# %%
df['release_date'] = pd.to_datetime(df['release_date'])
df['release_date']
# %%
similarity.shape
# %%
all = []

all_genres = df['genres'].apply(lambda x : [all.append(g) for g in x if g not in all])


# %%
len(all)
# %%
for a in df.itertuples():
    print(a)
# %%
df.columns
# %%

embed = np.load("/home/manraj_studios/Python/Movie-APP-v2/Data/story_genre_keywords.npy")
data = []
with open("/home/manraj_studios/Python/Movie-APP-v2/Data/User_Data.json" , 'r') as file:
    data = json.load(file)
# %%
watched = df[df['id'].isin(data[0]['watched'])]

# %%
watched_embed = embed[df[df['id'].isin(watched['id'])].index]
not_watched_embed = embed[df[~df['id'].isin(watched['id'])].index]

# %%
not_watched_movies = df[~df['id'].isin(watched['id'])]

# %%

similarity = cosine_similarity(watched_embed,not_watched_embed).mean(axis=0)
# %%
similarity_indices = similarity.argsort()[::-1][:10]
# %%
df.iloc[similarity_indices]
# %%
