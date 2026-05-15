import pandas as pd
from rapidfuzz import process,fuzz
from Movie_Recommendation_Manager import Recommendation_Manager

class Movie_Manager:
    def __init__(self,dataset):
        self.df = dataset
        self.recommendation_manager = Recommendation_Manager(self.df)
        
    def search_by_movie_name(self,movie_name):
        return process.extract(movie_name,self.df['original_title'],limit=5)
    
    def search_by_description(self,key_words,k=10):
        return self.recommendation_manager.compare_keywords(key_words,k)
    
    def based_previous_wacthes(self,previous_watches,k):
        recs:pd.DataFrame = self.recommendation_manager.previous_watches(previous_watches,k)
        recs = recs.sort_values(by='rating')
        return recs
    
    def filter_movies(self,genres:list,rating=5,vote=True):
        df:pd.DataFrame = self.df.copy()
        df = df[df['rating'] >= rating]
        df['genre_score'] = [sum(1 for g in cur if g in genres) for cur in df['genres']]
        df['norm_rating'] = df['rating']/10
        df['norm_genre_score'] = df['genre_score']/(df['genre_score'].to_numpy().max() + (1 if df['genre_score'].to_numpy().max() == 0 else 0))
        
        df['score'] = df['norm_genre_score'] * 0.6 + df['norm_rating'] * 0.4

        df = df.sort_values(by='score',ascending=False)

        return df.sort_values(by='votes',ascending=False) if vote else df.copy()

    def random_movie(self):
        return self.df.sample(1)
    
    def similar_to_movie(self,movie,k=10):
        return self.recommendation_manager.similar_to_X(movie,k)
    
    def similar_to_last_watched(self,previous_watches,k=10):
        return self.recommendation_manager.similar_to_X(previous_watches.iloc[-1],k)