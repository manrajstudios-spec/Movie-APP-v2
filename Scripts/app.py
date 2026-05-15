from flask import Flask,request,redirect,render_template

app = Flask(__name__,template_folder="templates")

@app.route("/base",meathods=["POST","GET"])
def base():
    if request.method == 'POST':
        value = request.form.get('value')