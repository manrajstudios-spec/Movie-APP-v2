# %%
import pandas as pd
import numpy as np
import ast
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# %%

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
df['story_genre'] = df['overview'] + " "+ "Genres: " + df['genre_text'] + " " +"Keywords : " + df['keywords_text']

# %%
pre = df[:10]

# %%
model = SentenceTransformer("all-MiniLM-L6-v2")

# %%
story_score = model.encode(df['story_genre'].to_list())

# %%
watched_story_score = model.encode(pre['story_genre'].to_list())

# %%
df = df[~df['id'].isin(pre['id'])].copy()

# %%
similarity = cosine_similarity(watched_story_score,story_score)[0]

# %%
similarity_indices = np.argsort(similarity)[::-1][:10]

# %%
df.iloc[similarity_indices]

# %%

