class User_Profile:
    def __init__(self,user_name,user_password,watched,watchlist):
        self.user_name = user_name
        self.user_password = user_password
        self.watched = watched
        self.watchlist = watchlist

    def return_user(self):
        return {'user_name':self.user_name,
                'user_password':self.user_password,
                'watched':self.watched,
                'watchlist':self.watchlist}