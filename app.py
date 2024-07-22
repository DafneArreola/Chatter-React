import os
import requests
import json
import base64
#from flask_behind_proxy import FlaskBehindProxy

from backend.comments_forms import CommentForm
from backend.spotify_authentication import create_spotify_login_link, callback_result
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, session, url_for, flash, redirect, Response
from flask_sqlalchemy import SQLAlchemy #NOTE: i am using the flask_sqlalchemy, but im sure this code can be reafactored to use the engine method from codio

template_dir = os.path.abspath('frontend/templates') # this just specifies the location of the templates folder, so you only have to put file name when using "render_template('File_name')"
app = Flask(__name__, template_folder=template_dir, static_folder='frontend/static')
app.secret_key = '257fdf6bda7c13f4f79223af7f8cdd3e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite'
#app.config['SQLALCHECMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    user_id = db.Column("user_id", db.String(100))
    comment = db.Column("comment", db.String(1000))
    timestamp = db.Column("timestamp", db.String(100))

    def __init__(self, comment, name, user_id, timestamp):
        self.name = name
        self.comment = comment
        self.user_id = user_id
        self.timestamp = timestamp


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
    #session.pop('access_token', None)
    #session.pop('refresh_token', None)
    #session.pop('expires_at', None)
    return render_template('music_home.html')


@app.route('/spotify_login')
def spotify_login():

    spotify_login_link_url = create_spotify_login_link(request.args.get('show_dialog'))
    return redirect(spotify_login_link_url)

@app.route('/callback')
def callback(): # this will handle both successful and unsuccessful login attempts
 
        callback_successful = callback_result(request=request, session=session)
        if callback_successful:
            return redirect(url_for('music_home2'))
        else:
            return {'error': request.args['error']}
        
@app.route('/music_home2')
def music_home2():
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    currently_playing_response = requests.get(API_BASE_URL + 'me/player/currently-playing', headers=headers)
    playback_status = None
    playback_status_return = {}
    if currently_playing_response.status_code == 204:
        flash("there is no media currently playing")
        print("there is no media currently playing")
    else:
        playback_status = currently_playing_response.json()
        playback_status_return['image'] = playback_status['item']['album']['images'][1]['url']
        playback_status_return['name'] = playback_status['item']['name']
        playback_status_return['id'] = playback_status['item']['id']
        playback_status_return['duration_ms'] = playback_status['item']['duration_ms']
        playback_status_return['progress_ms'] = playback_status['progress_ms']

        playback_status = playback_status_return


    #json.dumps(playback_status, indent=3)
    #with open("Output.txt", "a", encoding = "UTF-8") as f:
    #    f.write(json.dumps(playback_status, indent=3 ))
    
    
    return render_template('music_home2.html', playback_status=playback_status) 

@app.route('/music_player')      
def music_player():
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    currently_playing_response = requests.get(API_BASE_URL + 'me/player/currently-playing', headers=headers)
    playback_status_return = {}
    if currently_playing_response.status_code == 204:
        flash("there is no media currently playing")
        print("there is no media currently playing")
    else:
        playback_status = currently_playing_response.json()
        playback_status_return['image'] = playback_status['item']['album']['images'][1]['url']
        playback_status_return['name'] = playback_status['item']['name']
        playback_status_return['id'] = playback_status['item']['id']
        playback_status_return['duration_ms'] = playback_status['item']['duration_ms']
        playback_status_return['progress_ms'] = playback_status['progress_ms']

    return render_template('music_player.html', playback_status=playback_status_return)


@app.route('/control_playback', methods=['GET', 'POST'])
def control_playback():
    # "access_token" will only be in session if user is logged in
    if 'access_token' not in session:
        return redirect(url_for('spotify_login', show_dialog=False))

    # if token is expired, we will refresh it in the background (user will not need to login again)
    if datetime.now().timestamp() > session['expires_at']:
        print('token expired, refreshing.......')
        return redirect(url_for('spotify_refresh_token'))
    
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    
    # response = requests.get(API_BASE_URL + 'me/playlists', headers=headers)
    # playlists = response.json()

    currently_playing_response = requests.get(API_BASE_URL + 'me/player/currently-playing', headers=headers)
    playback_status = {'progress_ms': 0, 'item':{'duration_ms':1}}
    if currently_playing_response.status_code == 204:
        return Response(
            "There is no currently playing music",
            status=400,
        )
    else:
        playback_status = currently_playing_response.json()
    
    progress_ms = playback_status['progress_ms']
    duration_ms = playback_status['item']['duration_ms']

    return jsonify({'progress_ms': progress_ms,
                    'duration_ms': duration_ms
                    })
    


    # form = CommentForm()
    # if request.method == 'POST':
    #     if form.validate_on_submit():
    #         comment = request.form.get('comment')
    #         name = request.form.get('name')
    #         user_id = request.form.get('user_id')
    #         time_stamp = request.form.get('time_stamp')

    #         userr = users(comment, name, user_id, time_stamp)
    #         db.session.add(userr)
    #         db.session.commit()

    #         flash("user added succesfuly")

    # table_data = users.query.order_by(users.name)

    # return render_template('control_playback.html', content=playlists, playback_status=playback_status, table_data=table_data, form=form)

    #########################
    # CONTROL PLAYBACK HERE #
    #########################


@app.route('/spotify_refresh_token')
def spotify_refresh_token():
    if 'refresh_token' not in session:
        return redirect(url_for('spotify_login', show_dialog=False))
    
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

with app.app_context():
    users.query.delete()
    db.session.commit()
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")