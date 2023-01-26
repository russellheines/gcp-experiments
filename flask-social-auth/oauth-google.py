"""
Import necessary modules.
  - `os` to read env variable
  - `requests` to make GET/POST requests
"""
import os
import requests
from urllib.parse import parse_qs


"""
Define the GITHUB_ID and GITHUB_SECRET environment variables
along with the endpoints.
"""
CLIENT_ID = os.getenv("GOOGLE_ID")
CLIENT_SECRET = os.getenv("GOOGLE_SECRET")
AUTHORIZATION_ENDPOINT = f"https://accounts.google.com/o/oauth2/v2/auth?scope=https%3A//www.googleapis.com/auth/userinfo.email&redirect_uri=http%3A//127.0.0.1%3A5000/login/google/authorized&access_type=offline&response_type=code&client_id={os.getenv('GOOGLE_ID')}"
TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
USER_ENDPOINT = "https://www.googleapis.com/oauth2/v2/userinfo"


"""
1. Log in via the browser using the 'Authorization URL' outputted in the terminal.
   (If you're already logged in to Google, either log out or test in an incognito/private browser window.)
2. Once logged in, the page will redirect. Grab the code from the redirect URL.
3. Paste the code in the terminal.
"""
print(f"Authorization URL: {AUTHORIZATION_ENDPOINT}")
code = input("Enter the code: ")


"""
Using the authorization code, we can request an access token.
"""
# Once we get the code, we sent the code to the access token
# endpoint(along with id and secret). The response contains
# the access_token and we parse is using parse_qs
res = requests.post(
    TOKEN_ENDPOINT,
    data=dict(
        client_id=os.getenv("GOOGLE_ID"),
        client_secret=os.getenv("GOOGLE_SECRET"),
        redirect_uri='http://127.0.0.1:5000/login/google/authorized',
        grant_type='authorization_code',
        code=code,
    ),
)
data = res.json()
token = data["access_token"]

"""
Finally, we can use the access token to obtain information about the user.
"""
user_data = requests.get(USER_ENDPOINT, headers=dict(Authorization=f"Bearer {token}"))
print(user_data.content)
print(user_data.status_code)
username = user_data.json()["email"]
print(f"You are {username} on Google")