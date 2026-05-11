import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class recommendation_manager:
    def __init__(self,df):
        self.df = df.copy() 
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        np.save('Data/embeded_overview.npy',self.get_embeded_text(self.df['overview'].to_list()))
        self.overview_embed = self.load_embeddings()

    def get_embeded_text(self,to_embed):
        return self.model.encode(to_embed)
    
    def load_embeddings(self):
        return np.load("Data/embeded_overview.npy'")

    def compare_keywords(self,compare):
        compare = self.get_embeded_text([compare])
        
        similarity = cosine_similarity(compare,self.overview_embed)[0]
        