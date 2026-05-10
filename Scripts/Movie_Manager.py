from rapidfuzz import process,fuzz

class Movie_Manager:
    def __init__(self,dataset):
        self.df = dataset

    def search_by_movie_name(self,movie_name):
        return process.extract(movie_name,self.df['original_title'],limit=5)
    
    def search_by_description(self,key_words):
        pass