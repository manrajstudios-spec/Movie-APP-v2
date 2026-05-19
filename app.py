from flask import Flask, request, redirect, render_template,url_for,flash,session
from db import users_collection
from User_Saving import login_user,register_user,return_user,get_previous_watches,get_watchlist,add_to_watched,add_to_watchlist,watched_exists,watchlist_exists
from Data_Loader import return_dataset
from Movie_Manager import Movie_Manager
import webbrowser as wb
import os

app = Flask(__name__, template_folder="templates")
app.secret_key = "Manraj"

df = return_dataset()
movie_manager = Movie_Manager(df)

@app.route("/")
def start():
    return redirect(url_for("base"))


@app.route("/base", methods=["POST", "GET"])
def base():
    session.clear()
    if request.method == 'POST':
        value = request.form.get('rl')

        if value == "login":
            return redirect(url_for("login"))
        else:
            return redirect(url_for("register"))

    return render_template("base.html")

@app.route("/login",methods=["GET","POST"])
def login():
    session.clear()
    if request.method == "POST":
        user_name = request.form.get("user_name")
        user_password = request.form.get("user_password")

        if login_user(user_name,user_password):
            session["user_name"] = user_name
            return redirect(url_for("menu"))
        else:
            flash("Pasword dont match")
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/register",methods=["POST","GET"])
def register():
    session.clear()

    if request.method == "POST":
        user_name = request.form.get("user_name")
        user_password = request.form.get("user_password")
        confirm_password = request.form.get("confirm_password")

        if user_password != confirm_password:
            flash("Confirm Pasword dont match")
            return redirect(url_for("register"))
        else:      
            if register_user(user_name,user_password):
                session["user_name"] = user_name
                return redirect(url_for("menu"))
            else:
                flash("User Already Exits")
                return redirect(url_for("register"))
            
    return render_template("register.html")
        
@app.route("/base/menu",methods=["POST","GET"])
def menu():
    if request.method == "POST":
        options = request.form.get("options")
        movies = None
        match options:
            case "name":
                return redirect(url_for("search_name"))
            case "description":
                return redirect(url_for("search_description"))
            case "filter":
                return redirect(url_for("filter"))
            case "recs":
                if watched_exists(session.get('user_name')):
                    watched = get_previous_watches(session.get("user_name"),df=df)
                    movies = movie_manager.based_previous_wacthes(watched)
                else:
                    flash("No movies watched")
                    return redirect(url_for("menu"))
            case "random":
                movie = movie_manager.random_movie()
                session['movie_id'] = int(movie.iloc[0]['id'])
                return redirect(url_for('watch_movie'))
            case "surprise_me":
                if watchlist_exists(session.get('user_name')):
                    watchlist = get_watchlist(session.get("user_name"),df)
                    movies = movie_manager.similar_to_movie(watchlist.iloc[0])
                else:
                    flash("No movies in watch later")
                    return redirect(url_for("menu"))
            case "watchlist":
                if watchlist_exists(session.get('user_name')):
                    watchlist = get_watchlist(session["user_name"],df=df)
                    movies = watchlist
                else:
                    flash("No movies in watch later")
                    return redirect(url_for("menu"))

        session['movie_ids'] = movies["id"].to_list()
        return redirect(url_for("list_movies"))
    return render_template("menu.html")

@app.route("/base/menu/search_name",methods=["POST","GET"])
def search_name():
    if request.method == "POST":
        name = request.form.get("name")
        movies = movie_manager.search_by_movie_name(name)
        session["movie_ids"] = movies['id'].to_list()

        return redirect(url_for("list_movies"))

    return render_template("search_name.html")

@app.route("/base/menu/search_description",methods=["POST","GET"])
def search_description():
    if request.method == "POST":
        des = request.form.get("description")
        movies = movie_manager.search_by_description(des)
        session["movie_ids"] = movies['id'].to_list()

        if not movies.empty:
            return redirect(url_for("list_movies"))
    return render_template("search_description.html")

@app.route("/base/menu/filter",methods=["POST","GET"])
def filter():
    if request.method == "POST":
        selected_genres = request.form.getlist("genres")
        rating = request.form.get("rating")

        if not selected_genres:
            flash("No Genres Selected")
            return redirect(url_for("filter")) 
        else:
            movies = movie_manager.filter_movies(genres=selected_genres,rating=rating)
            session["movie_ids"] = movies['id'].to_list()
            return redirect(url_for("list_movies"))

    return render_template("filter.html")

@app.route("/base/menu/list_movies",methods=["POST","GET"])
def list_movies():
    movie_ids = session.get("movie_ids")
    movies = df[df["id"].isin(movie_ids)]

    if request.method == "POST":
        _id = int(request.form.get("movie"))

        session['movie_id'] = _id
        return redirect(url_for("watch_movie"))

    return render_template("list_movies.html",movies=movies.to_dict(orient="records"))

@app.route("/base/menu/watch_movie",methods=["POST","GET"])
def watch_movie():
    movie = df[df['id'] ==  session["movie_id"]]
    movie_dict = movie.iloc[0].to_dict()

    if request.method == "POST":
        val = request.form.get("action")

        if val == "play":
            search = movie_dict['title'] + " official trailer"
            url = f"https://www.youtube.com/results?search_query={search}"
            wb.open_new_tab(url)
            add_to_watched(int(movie.iloc[0]["id"]),session.get("user_name"))

        elif val == "similar":
            movies = movie_manager.similar_to_movie(movie_dict)
            session['movie_ids'] = movies['id'].to_list()
            return redirect("list_movies")
        elif val == "watchlist":
            add_to_watchlist(movie.iloc[0]["id"],session.get("user_name"))
        else:
            return redirect(url_for("review"))
    return render_template("watch_movie.html",movie=movie_dict)

@app.route("/base/menu/watch_movie/review",methods=["POST","GET"])
def review():
    movie = df[df['id'] ==  session["movie_id"]]
    movie_dict = movie.iloc[0].to_dict()

    if request.method == "POST":
        rating = request.form.get("rating")
        review = request.form.get("review")
        movie_manager.add_review(session.get("user_name"),int(rating),review,movie_title=movie_dict['title'],movie_id=movie_dict['id'])

    return render_template("review.html",movie=movie_dict)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)