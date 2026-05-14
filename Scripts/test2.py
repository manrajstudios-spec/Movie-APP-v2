from Movie_Recommendation_Manager import recommendation_manager
from Data_Loader import return_dataset

df = return_dataset()
keywords = "A Boy Falls In Love"

Recommendation_Manager = recommendation_manager(df)

print(df.iloc[Recommendation_Manager.compare_keywords(keywords)])