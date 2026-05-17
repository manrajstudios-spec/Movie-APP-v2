from flask import Flask, request, redirect, render_template,url_for,flash,session
from db import users_collection
from User_Saving import login_user,register_user,return_user
app = Flask(__name__, template_folder="templates")
app.secret_key = "Manraj"
@app.route("/")
def start():
    return redirect(url_for("base"))


@app.route("/base", methods=["POST", "GET"])
def base():
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
           redirect(url_for("menu"))
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
                return redirect(url_for("register"))
            else:
                flash("User Already Exits")
                return redirect(url_for("register"))
    return render_template("login.html")
        
@app.route("/base/menu",methods=["POST","GET"])
def menu():
    return render_template("menu.html")