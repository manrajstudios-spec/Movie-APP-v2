from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client["MovieAppV2"]

users_collection = db['users']

users_collection.create_index(
    "user_name",
    unique=True
)

print('connected')


