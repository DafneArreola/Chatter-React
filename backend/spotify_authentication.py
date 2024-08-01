import urllib.parse
import requests
from backend.config import Config
from datetime import datetime, timedelta
from backend.database import db
from backend.models import User

CLIENT_ID = Config.MUSIC_CLIENT_ID
CLIENT_SECRET = Config.MUSIC_CLIENT_SECRET
#REDIRECT_URI = 'https://ubiquitous-zebra-69v6q6qxw6pf4vgg-5000.app.github.dev/callback'
REDIRECT_URI = 'http://localhost:5000/callback'
# REDIRECT_URI = 'https://chatterreact.pythonanywhere.com/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token/' # used to obtain and refresh token
API_BASE_URL = 'https://api.spotify.com/v1/'


def create_spotify_login_link(show_dialog):
    scope = 'user-read-playback-state user-modify-playback-state user-read-currently-playing playlist-read-private user-read-email'

    params =  {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope' : scope,
        'redirect_uri': REDIRECT_URI,
        'show_dialog': show_dialog
    }

    return f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

def callback_result(request, session, user_id_var): # this will handle both successful and unsuccessful login attempts
    global CLIENT_ID
    global CLIENT_SECRET
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

        #print("{}:{}".format(CLIENT_ID, CLIENT_SECRET).encode())
        #formatted = "{}:{}".format(CLIENT_ID, CLIENT_SECRET).encode()
        #encoded = base64.b64encode(formatted)
        #headers = {"Content-Type" : 'application/x-www-form-urlencoded', 
        #           "Authorization" : "Basic {}".format(encoded)} 
        
        response = requests.post(TOKEN_URL, data=req_body)
        token_info = response.json()
        
        session['spotify_access_token'] = token_info['access_token']  # used to do tasks requiring auth (lasts a day)
        session['spotify_refresh_token'] = token_info['refresh_token']  # used to avoid user needing to login after token expires
        session['spotify_expires_at'] = datetime.now().timestamp() + token_info['expires_in']  # keeping track of when token expires
        session['user_id'] = user_id_var

        return True
    
def token_refresh_result(refresh_token):
    req_body = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }

    return requests.post(TOKEN_URL, data=req_body)

def get_current_track_info(spotify_access_token):
    headers = {
        'Authorization': f"Bearer {spotify_access_token}"
    }
    return requests.get(API_BASE_URL + 'me/player', headers=headers)



def put_play(spotify_access_token, device_id):
    headers = {
        'Authorization': f"Bearer {spotify_access_token}"
    }
    params = f'device_id={device_id}'

    return requests.put(API_BASE_URL + 'me/player/play' + '?' +  params, headers=headers)

def put_pause(spotify_access_token, device_id):
    headers = {
        'Authorization': f"Bearer {spotify_access_token}"
    }
    params = f'device_id={device_id}'

    return requests.put(API_BASE_URL + 'me/player/pause' + '?' +  params, headers=headers)



    