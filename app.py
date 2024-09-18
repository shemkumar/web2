from flask import Flask, request, render_template, make_response, redirect
import json
import jwt
import base64
import random
import os

app = Flask(__name__, template_folder='static')

SECRET_KEY = "lol"
ADMIN_PASSWORD = "thepasswordisnotea5ytog3tsohackthiswebsite"
FLAG = "root@localhost{P@ssw0rDS_r_0pti0n4l}"

@app.route('/', methods=['GET'])
def login_page():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def attempt_login():
    username = request.form['user']
    password = request.form['pass']

    if username == "demo" and password == "demo":
        pass
    elif username == "root@locahost" and password == ADMIN_PASSWORD:
        pass
    else:
        return "Invalid login."

    new_jwt = jwt.encode({"user": username}, SECRET_KEY)
    resp = make_response(redirect("/dashboard"))
    resp.set_cookie("token", new_jwt)
    return resp

@app.route('/dashboard', methods=['GET'])
def dashboard():
    token = request.cookies.get('token')

    if token is None:
        return redirect("/")

    claims = json.loads(base64.b64decode(token.split(".")[1] + "=="))
    user = claims['user']

    if user == "demo":
        status = "Welcome demo user! In the real app, you'd see your confidential system info here!"
    if user == "root@locahost":
        status = "Welcome, to student care tracking system just for 000000000000  Most recent system information: " + FLAG

    return render_template("dashboard.html", user=user, status=status)

app.run(host='0.0.0.0', port=2024)
