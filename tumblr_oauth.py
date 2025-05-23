import os
from dotenv import load_dotenv
from requests_oauthlib import OAuth1Session

load_dotenv()

consumer_key = os.getenv("TUMBLR_API_KEY")
consumer_secret = os.getenv("TUMBLR_API_SECRET")

print(f"Consumer Key: {consumer_key}")
print(f"Consumer Secret: {consumer_secret}")

request_token_url = "https://www.tumblr.com/oauth/request_token"
authorize_url = "https://www.tumblr.com/oauth/authorize"
access_token_url = "https://www.tumblr.com/oauth/access_token"

# Use 'oob' for PIN-based auth (out-of-band)
oauth = OAuth1Session(consumer_key, client_secret=consumer_secret, callback_uri='http://localhost:8080/')


# Step 1: Get request token
fetch_response = oauth.fetch_request_token(request_token_url)
resource_owner_key = fetch_response.get('oauth_token')
resource_owner_secret = fetch_response.get('oauth_token_secret')

print(f"Request Token: {resource_owner_key}")
print(f"Request Token Secret: {resource_owner_secret}")

# Step 2: Get user authorization URL and open it in your browser
authorization_url = oauth.authorization_url(authorize_url)
print(f"Please go here and authorize: {authorization_url}")

# Step 3: Get verifier (PIN) from user input
verifier = input('Paste the PIN here after authorization: ')

# Step 4: Get the access token using verifier
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=resource_owner_key,
    resource_owner_secret=resource_owner_secret,
    verifier=verifier,
)
oauth_tokens = oauth.fetch_access_token(access_token_url)

access_token = oauth_tokens['oauth_token']
access_token_secret = oauth_tokens['oauth_token_secret']

print(f"Access Token: {access_token}")
print(f"Access Token Secret: {access_token_secret}")
