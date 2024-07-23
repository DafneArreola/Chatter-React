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



######################
## HELPER FUNCTIONS ##
######################

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

# note: do not use '?' at end of path or beginning of params
def call_spotify_api(path, params):
    token = obtain_non_user_token()
    headers = {'Authorization': f"Bearer {token}"}
    return requests.get(API_BASE_URL + path + '?' +  params, headers=headers)

def create_artists_string(artists):
    artist_names_list = [artist['name'] for artist in artists]
    artist_names_str = ''
    for name in artist_names_list:
        artist_names_str += name + ', '
    return artist_names_str[:-2]

def convert_ms_to_time(ms):
    total_seconds = ms / 1000

    minutes = total_seconds // 60
    seconds = total_seconds - (minutes * 60)

    minutes = int(minutes)
    if minutes < 10:
        minutes = '0' + str(minutes)
    else:
        minutes = str(minutes)

    seconds = int(seconds)
    if seconds < 10:
        seconds = '0' + str(seconds)
    else:
        seconds = str(seconds)

    return f'{minutes}:{seconds}'



########################
## API CALL FUNCTIONS ##
########################

def get_home_tracks():
    ## INFO FOR "Today's Top Hits" PLAYLIST ##
    playlist_id="37i9dQZF1DXcBWIGoYBM5M"

    path = f'playlists/{playlist_id}/tracks' 
    params = 'limit=18'
    response = call_spotify_api(path, params)
    tracks = response.json()['items']

    filtered_tracks = []
    for track in tracks:
        new_entry={}
        new_entry['name'] = track['track']['name']
        new_entry['image'] = track['track']['album']['images'][1]['url']
        new_entry['id'] = track['track']['id']

        filtered_tracks.append(new_entry)

    return filtered_tracks   

def get_search_tracks(name):

    path = 'search' 
    params = f'q={name}&type=track&limit=50&market=US'
    response = call_spotify_api(path, params)
    print(response)
    if response.status_code != 200:
        return [False]
    tracks = response.json()['tracks']['items']

    filtered_tracks = []
    for track in tracks:
        new_entry = {}
        new_entry['name'] = track['name']
        new_entry['image'] = track['album']['images'][1]['url'] # returns image url that is 300px x 300px
        new_entry['id'] = track['id']
        new_entry['artists'] = create_artists_string(track['artists'])
        filtered_tracks.append(new_entry)
    
    return filtered_tracks

def get_track_info(id):

    path = f'tracks/{id}' 
    response = call_spotify_api(path, params='')
    track = response.json() 

    ## DELETE ## 
    del track['album']["available_markets"]
    del track["available_markets"]
    
    #json.dumps(response.json(), indent=3 )
    with open("Output.txt", "w", encoding = "UTF-8") as f:
        f.write(json.dumps(track, indent=3 ))
    ############   

    filtered_track={}
    filtered_track['id'] = track['id']
    filtered_track['name'] = track['name']
    filtered_track['image'] = track['album']['images'][1]['url']
    filtered_track['artists'] = create_artists_string(track['artists'])
    filtered_track['album_type'] = track['album']['album_type']
    filtered_track['album_name'] = track['album']['name']
    filtered_track['release_date'] = track['album']['release_date']
    filtered_track['duration'] = convert_ms_to_time(int(track['duration_ms']))
    filtered_track['duration_ms'] = track['duration_ms']

    print(filtered_track['album_type'])
    

    return filtered_track   


