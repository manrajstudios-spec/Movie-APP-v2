import pandas as pd
import webbrowser
from User_Saving import login_user,register_user,return_user,write_data
from Movie_Manager import Movie_Manager
from Data_Loader import return_dataset

df = return_dataset()
all_genres = ['Action',
 'Adventure',
 'Fantasy',
 'Science Fiction',
 'Crime',
 'Drama',
 'Thriller',
 'Animation',
 'Family',
 'Western',
 'Comedy',
 'Romance',
 'Horror',
 'Mystery',
 'History',
 'War',
 'Music',
 'Documentary',
 'Foreign',
 'TV Movie']
movie_manager = Movie_Manager(df)

def ask_user(to_ask):
    while True:
        user_input = input(to_ask)
        if user_input:
            return user_input

def filter_movies():
    while True:
        for i,genre in enumerate(all_genres):
            print(f"\n {i}: {genre} \n ")
        
        user_input = ask_user("Write The Number of genre as shown above --> example(0 1 2) for Action Adventure Fantasy\n")

        genres = []

        user_input = user_input.split(" ")

        for n in user_input:
            try:
                genres.append(all_genres[int(n)])
            except:
                pass

        genres = list(set(genres))

        rating = ask_user("Enter Rating Filter \n")

        if not rating.isdigit():
            continue

        votes_count = ask_user("0 for votes low to hight \n1 for high to low \n")

        if votes_count not in ['0','1']:
            continue

        return movie_manager.filter_movies(genres,int(rating),bool(int(votes_count)))

def watch_movie(movie,user):    
    while True:
        print(f"{movie['id']}: {movie['title']} \nDescription: {movie['overview']} \nRelease Date: {movie['release_date']} \nGenres: {movie['genres']} \nRating: {movie['rating']} Votes: {movie['vote_count']}")

        user_input = ask_user("\n1 Watch Movie \n2 Add To Watchlist \n3 To Rate And Write Review \nq to quit \n")

        if user_input == '1':            
            query = movie['title'] + " Trailer"
            url = f"https://www.youtube.com/results?search_query={query}"
            webbrowser.open(url)

            if int(movie['id']) not in user.watched:
                user.watched.append(int(movie['id']))

            if movie['id'] in user.watchlist:
                user.watchlist.remove(int(movie['id']))

            write_data(user.return_user())

        elif user_input == '2':
            if int(movie['id']) not in user.watchlist:
                user.watchlist.append(int(movie['id']))
                write_data(user.return_user())

        elif user_input == '3':
            rating = ask_user("Enter Rating you wanna give --> ")

            if rating.isdigit():
                if int(rating) > 10:
                    rating = 10

                review = ask_user("Enter Your Review \n")
                movie_manager.add_review(user.user_name,int(rating),review,movie['title'],movie['id'])
        elif user_input == 'q':
            break
                
def show_movies(movies:pd.DataFrame,user):
    if movies.empty:
        return
 
    while True:
        for index,movie in movies.iterrows():
            print(f"\n {movie['id']}: {movie['title']} \n {movie['overview']} \n")

        id = ask_user("Enter id of movie that you wanna watch \n Press q to quit \n")

        if id == 'q':
            break

        if id.isdigit():
            if int(id) in movies['id'].to_list():
                movie =  movies[movies['id'] == int(id)].iloc[0]

                if movie['id'] == int(id):
                    watch_movie(movie,user)

def menu(user):
    while True:
        user_input = ask_user(("""
                            🎬 MOVIE APP
                            ─────────────────
                            1. Search by Name
                            2. Search by Description
                            3. Filter Movies
                            4. Recommendations
                            5. Random Movie
                            6. Surprise Me
                            7. My Watchlist
                            8. Watch History
                            ─────────────────
                            q. Quit
                            """))
        
        movies = pd.DataFrame()

        match user_input:
            case '1':
                user_input = ask_user("Enter Movie Name \n")
                movies = movie_manager.search_by_movie_name(user_input)
            case '2':
                user_input = ask_user("Enter Movie Story Hint \n")
                movies = movie_manager.search_by_description(user_input)
            case '3':
                movies = filter_movies()
            case '4':
                watched = df[df['id'].isin(user.watched)]
                movies = movie_manager.based_previous_wacthes(watched)
            case '5':
                watch_movie(movie_manager.random_movie(),user) 
            case '6':
                watched = df[df['id'].isin(user.watched)]
                movies = movie_manager.similar_to_last_watched(watched)
            case '7':
                if user.watchlist:
                    movies = df[df['id'].isin(user.watchlist)]
            case '8':
                if user.watched:
                    movies = df[df['id'].isin(user.watched)]
            case 'q':
                break
        show_movies(movies,user)

def sign_in():
    user_name = ask_user("Enter Your User Name \n")
    user_password = ask_user("Enter Your Password \n")

    if login_user(user_name,user_password):
        menu(return_user(user_name,in_dict=False))
    else:
        print("wrong Password :( \n")

def sign_up():
    user_name = ask_user("Enter Your User Name \n")
    user_password = ask_user("Enter Your Password \n")

    if register_user(user_name,user_password):
        menu(return_user(user_name,in_dict=False))

while True:
    user_input = ask_user("1 To Login \n2 To Register \nq to quit \n")
    
    if user_input == '1':
        sign_in()
    elif user_input == '2':
        sign_up()
    elif user_input == 'q':
        break