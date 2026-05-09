import json

user_data_file = "Scripts/User_Saving.py"

def load_data():
    try:
        with open(user_data_file,'r') as file:
            return json.load(file)
    except:
        return []
    
def write_data(to_write):
    data = load_data()
    data.append(to_write)
    with open(user_data_file,'w')as file:
        json.dump(data,file,indent=4)

def check_user(user_name,user_password):
    data = load_data()

    if not data:
        return False
    
    for user in data:
        if user_name == user['user_name']:
            if user_password == user['user_password']:
                return True