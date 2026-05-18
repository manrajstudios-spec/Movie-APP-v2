from flask import Flask, request, redirect, render_template,url_for,flash,session
from db import users_collection
from User_Saving import login_user,register_user,return_user,get_previous_watches,get_watchlist
from Data_Loader import return_dataset
from Movie_Manager import Movie_Manager

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
            print("register")

    return render_template("base.html")

@app.route("/login",methods=["GET","POST"])
def login():
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
            
    return render_template("login.html")
        
@app.route("/base/menu",methods=["POST","GET"])
def menu():
    if request.method == "POST":
        options = request.form.get("options")

        match options:
            case "name":
                return redirect(url_for("/base/menu/search_name"))
            case "description":
                return redirect(url_for("/base/menu/search_description"))
            case "filter":
                return redirect(url_for("/base/menu/filter"))
            case "recs":
                watched = get_previous_watches(session.get("user_name"),df=df)
                movies = movie_manager.based_previous_wacthes(watched)
            case "random":
                movie = movie_manager.random_movie()
            case "surprise_me":
                if get_watchlist():
                    movies = get_watchlist()
            case "watchlist":
                watchlist = get_watchlist(session["user_name"],df=df)
                movies = watchlist.copy()
                
    return render_template("menu.html")

@app.route("/base/menu/search_name",methods=["POST","GET"])
def search_name():
    if request.method == "POST":
        name = request.form.get("name")
        movies = movie_manager.search_by_movie_name(name)

    return render_template("search_name.html")

@app.route("/base/menu/search_description",methods=["POST","GET"])
def search_description():
    if request.method == "POST":
        des = request.form.get("description")
        movies = movie_manager.search_by_description(des)
        
    return render_template("search_description.html")

@app.route("/base/menu/search_description",methods=["POST","GET"])
def search_description():
    if request.method == "POST":
        selected_genres = request.form.getlist("genres")
        rating = request.form.get("rating")

        if not selected_genres:
            flash("No Genres Selected")
            return redirect(url_for("filter")) 
        else:
            movies = movie_manager.filter_movies(genres=selected_genres,rating=rating)

    return render_template("filter.html")

