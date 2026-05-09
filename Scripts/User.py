
class User_Profile:
    def __init__(self,user_name,user_password):
        self.user_name = user_name
        self.user_password = user_password
        self.movie_data = []

    def return_user(self,user_data):
        return {'user_name':self.user_name,
                'user_password':self.user_password,
                'movie_data':self.movie_data}