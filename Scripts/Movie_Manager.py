import pandas as pd
import json
from rapidfuzz import process,fuzz
from Movie_Recommendation_Manager import Recommendation_Manager
from Data_Loader import return_dataset
from db import review_collection
import os
import requests
from dotenv import load_dotenv


class Movie_Manager:
    load_dotenv()

    TMDB_API_KEY = os.getenv("TMDB_API_KEY")

    def __init__(self,dataset):
        self.df = dataset
        self.recommendation_manager = Recommendation_Manager(self.df)
        self.tmdb_api_key = self.TMDB_API_KEY

    def search_by_movie_name(self,movie_name,k=5):
        names = process.extract(movie_name,self.df['title'],limit=k)
        names_only = [match[0] for match in names]
        df_names = self.df[self.df['title'].isin(names_only)]
        return df_names
    
    def search_by_description(self,key_words,k=10):
        return self.recommendation_manager.compare_keywords(key_words,k)
    
    def based_previous_wacthes(self,previous_watches,k=10):
        recs:pd.DataFrame = self.recommendation_manager.previous_watches(previous_watches,k)
        recs = recs.sort_values(by='rating',ascending=False)
        return recs

    def filter_movies(self,genres:list,rating=5,vote=True,k=10):
        df:pd.DataFrame = self.df.copy()
        df = df[df['rating'] >= rating]
        df['genre_score'] = [sum(1 for g in cur if g in genres) for cur in df['genres']]
        df['norm_rating'] = df['rating']/10
        df['norm_genre_score'] = df['genre_score']/(df['genre_score'].to_numpy().max() + (1 if df['genre_score'].to_numpy().max() == 0 else 0))
        
        df['score'] = df['norm_genre_score'] * 0.6 + df['norm_rating'] * 0.4

        df = df.sort_values(by='score',ascending=False)
        df = df.sort_values(by='vote_count',ascending=False) if vote else df.copy()
        return df[:k]

    def random_movie(self):
        return self.df.sample(1)
    
    def similar_to_movie(self,movie,k=10):
        return self.recommendation_manager.similar_to_X(movie,k)
    
    def similar_to_last_watched(self,previous_watches,k=10):
        return self.recommendation_manager.similar_to_X(previous_watches.iloc[-1],k)
    
    def add_review(self,user_name,rating,r,movie_title,movie_id):      
        movie = review_collection.find_one[{'movie_id':movie_id}]

        if movie:
            review_collection.update_one({"movie_id": movie_id},{"$push": {"reviews": {"user_name": user_name,"rating": rating,"review": r}}})
        else:
            review_collection.insert_one({"movie_id":movie_id,"movie_title":movie_title,"reviews":[{"user_name":user_name,"rating":int(rating),"review":r}]})         
            
    def get_movie_poster(self, movie_id):

        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={self.tmdb_api_key}"

        response = requests.get(url)

        data = response.json()

        poster_path = data.get("poster_path")

        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"

        return None
    

