from User_Saving import login_user,register_user

def ask_user(to_ask):
    while True:
        user_input = input(to_ask)
        if user_input:
            return user_input

def menu():
    pass
      
def sign_in():
    user_name = ask_user("Enter Your User Name \n")
    user_password = ask_user("Enter Your Password \n")

    login_user(user_name,user_password)

def sign_up():
    user_name = ask_user("Enter Your User Name \n")
    user_password = ask_user("Enter Your Password \n")

    register_user(user_name,user_password)
    

while True:
    user_input = ask_user("1 To Login \n2 To Register \nq to quit \n")
    
    if user_input == '1':
        sign_in()
    elif user_input == '2':
        sign_up()
    elif user_input == 'q':
        break