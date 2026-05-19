import bcrypt
import json
from User import User_Profile
from db import users_collection

def return_user(user_name,in_dict=False):
    user_mongo = users_collection.find_one({"user_name":user_name})

    if not user_mongo : return False

    user = User_Profile(user_mongo['user_name'],user_mongo['user_password'],user_mongo['watched'],user_mongo['watchlist'])
    
    if in_dict:
        return user.return_user()
    else:
        return user

            
def check_user(user_name):
    user = users_collection.find_one({
        "user_name":user_name
    })

    return user is not None

def login_user(user_name, user_pass):

    user = users_collection.find_one({"user_name": user_name})

    if not user:
        return False

    return bcrypt.checkpw(
        user_pass.encode(),
        user['user_password'].encode()
    )

def register_user(user_name,user_pass):
    if check_user(user_name):
        return False

    hashed = bcrypt.hashpw(user_pass.encode(),bcrypt.gensalt()).decode()

    user = User_Profile(user_name,hashed,[],[])

    users_collection.insert_one(user.return_user())

    return True

def update_user(user_dict):
    users_collection.update_one({"user_name":user_dict['user_name']},
                                {"$set":
                                 {
                                     'watched':user_dict['watched'],
                                     'watchlist':user_dict['watchlist']
                                 }})

import pandas as pd

def get_previous_watches(user_name,df:pd.DataFrame):
    user = users_collection.find_one({"user_name":user_name})

    if user:
        ids = user["watched"]
        return df[df["id"].isin(ids)]

def get_watchlist(user_name,df:pd.DataFrame):
    user = users_collection.find_one({"user_name":user_name})

    ids = user["watchlist"]
    return df[df["id"].isin(ids)]


def watchlist_exists(user_name):
    user = users_collection.find_one({"user_name":user_name})

    return user['watchlist']

def watched_exists(user_name):
    user = users_collection.find_one({"user_name":user_name})

    return user['watched']

def add_to_watched(_id,user_name):
   users_collection.update_one({"user_name": user_name},{"$addToSet": {"watched": int(_id)},"$pull": {"watchlist": int(_id)}})

def add_to_watchlist(_id,user_name):
    users_collection.update_one({"user_name":user_name},
                                       {"$addToSet": {"watchlist": int(_id)}})
    