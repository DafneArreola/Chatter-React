import urllib.parse
import requests
from datetime import datetime, timedelta

CLIENT_ID = '1a9bd2df8c6c44afbbf527403e7306e3'
CLIENT_SECRET = 'edb1c825d83f4719b733d3b8ed05a4e9'
REDIRECT_URI = 'http://localhost:5000/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token/' # used to obtain and refresh token
API_BASE_URL = 'https://api.spotify.com/v1/'



def create_spotify_login_link():
    scope = 'user-read-playback-state user-modify-playback-state user-read-currently-playing playlist-read-private user-read-email'

    params =  {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope' : scope,
        'redirect_uri': REDIRECT_URI,
    }

    return f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

def callback_result(request, session): # this will handle both successful and unsuccessful login attempts
    global CLIENT_ID
    global CLIENT_SECRET
    ###flash(request.args)
    if 'error' in request.args:
        # if uncessful login attempt, we will simply return error as a json object
        print("ERROR FOUND IN REQUEST")
        return False
    
    if 'code' in request.args:
        #if successful login, we will use info to get token for the user so we can access playback features, and redirect user to __ page
        req_body = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }

        print("{}:{}".format(CLIENT_ID, CLIENT_SECRET).encode())
        #formatted = "{}:{}".format(CLIENT_ID, CLIENT_SECRET).encode()
        #encoded = base64.b64encode(formatted)
        #headers = {"Content-Type" : 'application/x-www-form-urlencoded', 
        #           "Authorization" : "Basic {}".format(encoded)} 
        
        response = requests.post(TOKEN_URL, data=req_body)
        token_info = response.json()

        session['access_token'] = token_info['access_token']  # used to do tasks requiring auth (lasts a day)
        session['refresh_token'] = token_info['refresh_token']  # used to avoid user needing to login after token expires
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']  # keeping track of when token expires

        return True