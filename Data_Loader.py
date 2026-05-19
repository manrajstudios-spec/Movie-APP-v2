import pandas as pd
import ast

def return_dataset():
    df = pd.read_csv("Data/movie_dataset.csv")
    clean_dataset(df)
    return df

def clean_dataset(df:pd.DataFrame):
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
    
    df['genre_text'] = df['genres'].apply(lambda x : ",".join(g for g in x))
    df['keywords_text'] = df['keywords'].apply(lambda x : ",".join(k for k in x)) 

    df['story_genre_keywords'] = df['overview'] + " "+ "Genres: " + df['genre_text'] + " " + "Key Words: " + df['keywords_text']

    df['release_date'] = pd.to_datetime(df['release_date'])

