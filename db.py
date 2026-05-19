from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(
    os.getenv("MONGODB_URI"),
    tlsAllowInvalidCertificates=True
)
db = client["MovieAppV2"]

users_collection = db['users']
review_collection = db['reviews']

users_collection.create_index("user_name",unique=True)

review_collection.create_index("movie_id",unique=True)

print('connected')


