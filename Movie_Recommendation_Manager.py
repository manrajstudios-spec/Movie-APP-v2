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
        print("Before Load")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        print("After Load")
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
        print("Embeddings Loaded")

    def compare_keywords(self,compare,k=10):
        compare = self.get_embeded_text([compare])
        
        overview_smilarity = cosine_similarity(compare,self.embeded_discription)[0]
        
        return self.df.iloc[np.argsort(overview_smilarity)[::-1][:k]]
    
    def previous_watches(self, previous_watches: pd.DataFrame, k=10):
        previous_watches_story_embed = self.story_embed[self.df[self.df['id'].isin(previous_watches['id'])].index]
        
        unwatched_df = self.df[~self.df['id'].isin(previous_watches['id'])]
        watched_story_embed = self.story_embed[unwatched_df.index]
        
        similarity = cosine_similarity(previous_watches_story_embed, watched_story_embed)
        similarity = similarity.mean(axis=0)
        
        similarity_indices = similarity.argsort()[::-1][:k]
        
        return unwatched_df.iloc[similarity_indices]

    def similar_to_X(self, movie, k=10):
        movie_embed = self.story_embed[self.df[self.df['id'] == movie['id']].index]

        excluded_df = self.df[~(self.df['id'] == movie['id'])]
        excluded_embed = self.story_embed[excluded_df.index]

        similarity = cosine_similarity(movie_embed, excluded_embed)[0]
        similarity_indices = similarity.argsort()[::-1][:k]

        return excluded_df.iloc[similarity_indices]
    
