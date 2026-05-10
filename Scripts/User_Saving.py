import bcrypt
import json
from User import User_Profile

user_data_file = "Data/User_Data.json"

def load_data():
    try:
        with open(user_data_file,'r') as file:
            return json.load(file)
    except:
        return []
    
def write_data(to_write):
    if check_user(to_write['user_name']):
        pass
    else:
        data = load_data()
        data.append(to_write)
        with open(user_data_file,'w')as file:
            json.dump(data,file,indent=4)

def return_user(user_name,in_dict=False):
    data = load_data()
    if not data:
        return False

    for user in data:
        if user['user_name'] == user_name:
            user = User_Profile(user_name,user['user_password'])

            if in_dict:
                return user.return_user()
            else:
                return user
            
def check_user(user_name):
    data = load_data()

    if not data:
        return False
    
    for user in data:
        if user_name == user['user_name']:
            return True
        
    return False

def login_user(user_name,user_pass):
    if check_user(user_name):
        if bcrypt.checkpw(user_pass.encode(),return_user(user_name,in_dict=True)['user_password'].encode()):
            return True
        
    return False

def register_user(user_name,user_pass):
    if not check_user(user_name):
        hashed = bcrypt.hashpw(user_pass.encode(),bcrypt.gensalt())

        user = User_Profile(user_name,hashed.decode())
        user_dict = user.return_user()

        write_data(user_dict)