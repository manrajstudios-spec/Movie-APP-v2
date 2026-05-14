# %%
import pandas as pd
import ast
from sentence_transformers import SentenceTransformer

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
pre = df[:10]

# %%
genres = []

for genre in pre.genres.to_list():
    for g in genre:
        if g in genres:
            continue
        genres.append(g)

# %%


