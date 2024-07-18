import os
import urllib.parse
import requests
import json
import base64
#from flask_behind_proxy import FlaskBehindProxy

from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, session, url_for, flash, redirect




template_dir = os.path.abspath('frontend/templates') # this just specifies the location of the templates folder, so you only have to put file name when using "render_template('File_name')"
app = Flask(__name__, template_folder=template_dir)
app.secret_key = '257fdf6bda7c13f4f79223af7f8cdd3e'

CLIENT_ID = '1a9bd2df8c6c44afbbf527403e7306e3'
CLIENT_SECRET = 'edb1c825d83f4719b733d3b8ed05a4e9'
REDIRECT_URI = 'http://localhost:5000/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token/' # used to obtain and refresh token
API_BASE_URL = 'https://api.spotify.com/v1/'

@app.route('/')
def start():
    return render_template('home.html')

@app.route('/music_home')
def music_home():
    return render_template('music_home.html')

@app.route('/spotify_login')
def spotify_login():
    scope = 'user-read-playback-state user-modify-playback-state user-read-currently-playing playlist-read-private user-read-email'

    params =  {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope' : scope,
        'redirect_uri': REDIRECT_URI,
    }

    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    print(auth_url)

    print(auth_url)
    return redirect(auth_url)

    #return redirect(url_for())

@app.route('/callback')
def callback(): # this will handle both successful and unsuccessful login attempts
    print("REACHED CALLBACKKKKKKKKKKKKKKKKKKKKKKKKKK")
    global CLIENT_ID
    global CLIENT_SECRET
    flash(request.args)
    if 'error' in request.args:
        # if uncessful login attempt, we will simply return error as a json object
        print("ERROR FOUND IN REQUEST")
        return {'error': request.args['error']}
    
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
        print("########################")
        print(token_info)
        print("########################")

        session['access_token'] = token_info['access_token']  # used to do tasks requiring auth (lasts a day)
        session['refresh_token'] = token_info['refresh_token']  # used to avoid user needing to login after token expires
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']  # keeping track of when token expires

        return redirect(url_for('control_playback'))

@app.route('/control_playback')
def control_playback():
    # "access_token" will only be in session if user is logged in
    if 'access_token' not in session:
        return redirect(url_for('spotify_login'))

    # if token is expired, we will refresh it in the background (user will not need to login again)
    if datetime.now().timestamp() > session['expires_at']:
        return redirect(url_for('spotify_refresh_token'))
    
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    
    response = requests.get(API_BASE_URL + 'me/playlists', headers=headers)
    playlists = response.json()
    print(playlists)

    return render_template('control_playback.html', content=playlists)

    #########################
    # CONTROL PLAYBACK HERE #
    #########################


@app.route('/spotify_refresh_token')
def spotify_refresh_token():
    if 'refresh_token' not in session:
        return redirect(url_for('spotify_login'))
    
    req_body = {
        'grant_type': 'refresh_token',
        'refresh_token': session['refresh_token'],
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }

    response = requests.post(TOKEN_URL, data=req_body)
    new_token_info = response.json()

    session['access_token'] = new_token_info['access_token']  # used to do tasks requiring auth (lasts a day)
    session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_at']  # keeping track of when token expires

    return redirect('/control_playback')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
