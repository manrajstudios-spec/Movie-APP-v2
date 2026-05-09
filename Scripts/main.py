
def ask_user(to_ask):
    while True:
        user_input = input(to_ask)
        if user_input:
            return user_input
        
def login_user():
    user_name = ask_user("Enter Your User Name \n")
    user_password = ask_user("Enter Your Password \n")

    if user_name and user_password:
        pass

def regitser_user():
    pass

while True:
    user_input = ask_user("1 To Login \n2 To Register \nq to quit \n")
    
    if user_input == '1':
        login_user()
    elif user_input == '2':
        regitser_user()
    elif user_input == 'q':
        break