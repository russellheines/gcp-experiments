from flask import Flask, render_template, redirect, request, make_response
import os
import requests
from urllib.parse import parse_qs

app = Flask(__name__)

@app.route("/")
def index():
    name = request.cookies.get("name")
    return render_template("index.html", fullname=name)

@app.route("/login/github")
def logingithub():
    AUTHORIZATION_ENDPOINT = f"https://github.com/login/oauth/authorize?response_type=code&client_id={os.getenv('GITHUB_ID')}"
    return redirect(AUTHORIZATION_ENDPOINT)

@app.route("/login/google")
def logingoogle():
    AUTHORIZATION_ENDPOINT = f"https://accounts.google.com/o/oauth2/v2/auth?scope=https%3A//www.googleapis.com/auth/userinfo.email+https%3A//www.googleapis.com/auth/userinfo.profile&redirect_uri={os.getenv('GOOGLE_REDIRECT_URL')}&access_type=offline&response_type=code&client_id={os.getenv('GOOGLE_ID')}"
    return redirect(AUTHORIZATION_ENDPOINT)

@app.route("/login/github/authorized")
def codegithub():
    TOKEN_ENDPOINT = "https://github.com/login/oauth/access_token"
    USER_ENDPOINT = "https://api.github.com/user"
    USERS_ENDPOINT = "https://api.github.com/users"

    # use authorization code to get a token
    res = requests.post(
        TOKEN_ENDPOINT,
        data=dict(
            client_id=os.getenv("GITHUB_ID"),
            client_secret=os.getenv("GITHUB_SECRET"),
            code=request.args.get('code'),
        ),
    )
    res = parse_qs(res.content.decode("utf-8"))
    token = res["access_token"][0]

    # use token to get user's full name
    user_data = requests.get(USER_ENDPOINT, headers=dict(Authorization=f"Bearer {token}"))
    login = user_data.json()["login"]

    users_data = requests.get(USERS_ENDPOINT + "/" + login, headers=dict(Authorization=f"Bearer {token}"))
    name = users_data.json()["name"]

    resp = make_response(redirect("/"))
    resp.set_cookie('name', name, httponly=True, secure=True)
    return resp

@app.route("/login/google/authorized")
def codegoogle():
    TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
    USERINFO_ENDPOINT = "https://www.googleapis.com/oauth2/v2/userinfo"

    # use authorization code to get a token
    res = requests.post(
        TOKEN_ENDPOINT,
        data=dict(
            client_id=os.getenv("GOOGLE_ID"),
            client_secret=os.getenv("GOOGLE_SECRET"),
            redirect_uri=os.getenv("GOOGLE_REDIRECT_URL"),
            grant_type='authorization_code',
            code=request.args.get('code'),
        ),
    )
    data = res.json()
    token = data["access_token"]

    # use token to get user's full name
    user_data = requests.get(USERINFO_ENDPOINT, headers=dict(Authorization=f"Bearer {token}"))
    name = user_data.json()["name"]

    resp = make_response(redirect("/"))
    resp.set_cookie('name', name, httponly=True, secure=True)
    return resp

@app.route("/logout")
def logout():
    resp = make_response(redirect("/"))
    resp.set_cookie('name', '', expires=0)
    return resp

# This is only used when running locally. When running live, gunicorn runs
# the application.
if __name__ == "__main__":
    app.run(debug=True)