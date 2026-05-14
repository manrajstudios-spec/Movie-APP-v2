import pandas as pd
import ast

def return_dataset():
    df = pd.read_csv("Data/movie_dataset")
    clean_dataset(df)
    return df

def clean_dataset(df):
    rating = df['vote_average']
    df = df.drop(columns=['vote_average'])
    df['rating'] = rating

    df['production_countries'] = df['production_countries'].apply(lambda x : ast.literal_eval(x))
    df['production_countries'] = df['production_countries'].apply(lambda x :[g['name'].strip() for g in x if 'name' in g])

    df['genres'] = df['genres'].apply(lambda x:ast.literal_eval(x))
    df['genres'] = df['genres'].apply(lambda x:[g['name'].strip() for g in x if 'name' in g])

    df['production_companies'] = df['production_companies'].apply(lambda x : ast.literal_eval(x))
    df['production_companies'] = df['production_companies'].apply(lambda x :[g['name'].strip() for g in x if 'name' in g])

    df['spoken_languages'] = df['spoken_languages'].apply(lambda x : ast.literal_eval(x))
    df['spoken_languages'] = df['spoken_languages'].apply(lambda x :[g['name'].strip() for g in x if 'name' in g])

    df['keywords'] = df['keywords'].apply(lambda x : ast.literal_eval(x))
    df['keywords'] = df['keywords'].apply(lambda x :[g['name'].strip() for g in x if 'name' in g])