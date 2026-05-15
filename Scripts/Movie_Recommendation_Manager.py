import numpy as np
import os
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class Recommendation_Manager:
    embeded_description_file = "Data/embeded_overview.npy"
    embeded_story_file = "Data/story_genre_keywords.npy"

    def __init__(self,df):
        self.df = df.copy() 
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.load_embeddings()
        
    def get_embeded_text(self,to_embed):
        return self.model.encode(to_embed)
    
    def load_embeddings(self):
        if not os.path.exists(self.embeded_description_file):
            np.save(self.embeded_description_file,self.model.encode(self.df['overview']))

        if not os.path.exists(self.embeded_story_file):
            np.save(self.embeded_story_file,self.model.encode(self.df['story_genre_keywords']))

        self.embeded_discription = np.load(self.embeded_description_file)
        self.story_embed = np.load(self.embeded_story_file)

    def compare_keywords(self,compare,k=10):
        compare = self.get_embeded_text([compare])
        
        overview_smilarity = cosine_similarity(compare,self.embeded_discription)[0]
        
        return np.argsort(overview_smilarity)[::-1][:k]
    
    def previous_watches(self,previous_watches:pd.DataFrame,k=10):
        previous_watches_story_embed = self.story_embed[self.df[self.df['id'].isin(previous_watches['id'])].index]
        watched_story_embed = self.story_embed[self.df[~self.df['id'].isin(previous_watches['id'])].index]
        
        similarity = cosine_similarity(previous_watches_story_embed,watched_story_embed)
        similarity = similarity.mean(axis=0) # we get how much each not watched movie is similar to watched 
        similarity_indices = similarity.argsort()[::-1][:k]

        return self.df.iloc[similarity_indices]

    def similar_to_X(self,movie,k=10):
        movie_embed = self.story_embed[self.df[self.df['id'] == movie['id']].index]
        other_movie_embed = self.story_embed[self.df[~(self.df['id'] == movie['id'])].index]
        similarity = cosine_similarity(movie_embed,other_movie_embed)[0]

        similarity_indices = similarity.argsort()[::-1][:k]
        
        return self.df.iloc[similarity_indices]