import requests
from backend.config import Config  # keys and stuff should be moved here
import json
import pprint

CLIENT_ID = Config.MUSIC_CLIENT_ID
CLIENT_SECRET = Config.MUSIC_CLIENT_SECRET
REDIRECT_URI = 'http://localhost:5000/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token/'  # used to obtain and refresh token
API_BASE_URL = 'https://api.spotify.com/v1/'


def obtain_non_user_token():
      # request params to obrain access_token to make NON PERMISSION calls
    req_body = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    headers = {"Content-Type" : 'application/x-www-form-urlencoded'}

    response = requests.post(TOKEN_URL, data=req_body, headers=headers)
    token = response.json()['access_token']

    return token


def get_home_tracks():
    ## INFO FOR "Today's Top Hits" PLAYLIST ##
    playlist_id="37i9dQZF1DXcBWIGoYBM5M"

    token = obtain_non_user_token()
    headers = {'Authorization': f"Bearer {token}"}
    
    response = requests.get(API_BASE_URL + f'playlists/{playlist_id}/tracks?limit=18', headers=headers)
    tracks = response.json()['items']

    filtered_tracks = []
    for track in tracks:
        new_entry={}
        new_entry['name'] = track['track']['name']
        new_entry['image'] = track['track']['album']['images'][1]['url']

        filtered_tracks.append(new_entry)
    
    #json.dumps(response.json(), indent=3 )
    #with open("Output.txt", "a", encoding = "UTF-8") as f:
    #    f.write(json.dumps(filtered_tracks, indent=3 ))

    return filtered_tracks   

get_home_tracks()
