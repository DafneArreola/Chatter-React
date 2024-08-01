from backend.movie_api import fetch_movies, search_movies, fetch_discover_movies, fetch_movie_details
import flask
from flask import Blueprint, request, render_template, flash,  session, url_for, redirect, Flask, jsonify
from backend.database import db
from backend.tv_show_api import get_popular_tv_shows_for_carousel
from backend.music_api import get_home_tracks, get_search_tracks, get_track_info
from backend.search_form import SearchForm
from werkzeug.security import generate_password_hash, check_password_hash
from backend.models import User, Comment, Rating, Media
from backend.tv_show_api import get_popular_tv_shows_for_carousel, get_tv_show_details, fetch_show_details, fetch_episode_details, search_tv_shows, get_popular_tv_shows, fetch_season_episodes, fetch_show_poster, fetch_shows
from datetime import timedelta
from collections import defaultdict
import requests
import json
import datetime

from backend.spotify_authentication import create_spotify_login_link, callback_result, token_refresh_result, get_current_track_info, put_pause, put_play

USER_ID = False

main = Blueprint('main', __name__)



@main.route('/')
def home():
    db.session.commit()
    global USER_ID

    if 'user_id' in session:
        USER_ID = session['user_id']
        print(True)
    else:
        USER_ID = None
        print(False)

    movies = fetch_movies()
    tracks = get_home_tracks()
    shows = fetch_shows()
    return render_template('home.html', movies=movies, tracks=tracks, shows=shows)

######################################
##########SPOTIFY LOGIN###############
######################################
@main.route('/spotify_login')
def spotify_login():

    spotify_login_link_url = create_spotify_login_link(show_dialog=request.args.get('show_dialog'))
    return redirect(spotify_login_link_url)

@main.route('/callback')
def callback(): # this will handle both successful and unsuccessful login attempts
    global USER_ID
    ### for some reason, the deletes the session when it reaches this route ###
    ## i ended up redifining the entire session in the "callback_result" function

    callback_successful = callback_result(request=request, session=session, user_id_var=USER_ID)

    if callback_successful:
        user = db.session.query(User).filter(User.id == USER_ID).first()
        print(user)
        print(user.username)
        user.spotify_access_token = session['spotify_access_token']  # used to do tasks requiring auth (lasts a day)
        user.spotify_refresh_token = session['spotify_refresh_token']  # used to avoid user needing to login after token expires
        user.spotify_expires_at = session['spotify_expires_at']  # used to avoid user needing to login after token expires
        return redirect(url_for('main.music_search', came_from_callback=True))
       
    else:
        return {'error': request.args['error']} 
######################################
##########SPOTIFY LOGIN###############
######################################


@main.route('/music', methods=['GET', 'POST'])
def music_search():
    user_id = session.get('user_id', None)
    #if 'user_id' not in session:
    if user_id == None:
        print('reached if')
        print(user_id)
        return redirect(url_for('main.login'))

    print("MADE IT BACK TO MUSIC Search")
    came_from_callback = request.args.get('came_from_callback', None)
    if came_from_callback:
        global USER_ID
        USER_ID = session['user_id']
        user = db.session.query(User).filter(User.id == session['user_id']).first()
        user.spotify_access_token = session['spotify_access_token']  # used to do tasks requiring auth (lasts a day)
        user.spotify_refresh_token = session['spotify_refresh_token']  # used to avoid user needing to login after token expires
        user.spotify_expires_at = session['spotify_expires_at']  # used to avoid user needing to login after token expires
        db.session.commit()
        print(user.id)
        print(user.spotify_access_token)
        print(user.spotify_refresh_token)
        print(user.spotify_expires_at)

    user_signed_in_to_chatter = 'user_id' in session
    user_id = session['user_id']
    user_signed_in_to_spotify = None

    if user_signed_in_to_chatter:
        user = db.session.query(User).filter(User.id == session['user_id']).first()
        user_signed_in_to_spotify = user.spotify_access_token  != None
        
    form = SearchForm()
    results = []

    if form.validate_on_submit():
        results = get_search_tracks(form.name_search.data)
        # i made it so that if there are no tracks for the search, the following will be returned: [False]
        if len(results) == 1 and results[0] == False:
            results = 'Result Not Found'
        search_query = form.name_search.data
    else:
        results = get_home_tracks()
        search_query = None
        
    return render_template('music_search.html', results=results, form=form, search_query=search_query, user_signed_in_to_chatter=user_signed_in_to_chatter, user_signed_in_to_spotify=user_signed_in_to_spotify, user_id=user_id)

@main.route('/music_player')      
def music_player():
    user = db.session.query(User).filter(User.id == session['user_id']).first()

    print('got to get_live_player screen')


    if user.spotify_access_token == None:
        return redirect(url_for('spotify_login', show_dialog=False))
    print(f"what is currently on db {datetime.datetime.now().timestamp()}")
    print(f"current time {user.spotify_expires_at}")
    print(f' token expires AFTER current time:{datetime.datetime.now().timestamp() > user.spotify_expires_at}')

    # if token is expired, we will refresh it in the background (user will not need to login again)
    if datetime.datetime.now().timestamp() > float(user.spotify_expires_at):
        print('token expired, refreshing.......')
        return redirect(url_for('main.spotify_refresh_token'))


    session['spotify_access_token'] = user.spotify_access_token
    session['spotify_expires_at'] = user.spotify_expires_at
    access_token = user.spotify_access_token
    currently_playing_response = get_current_track_info(access_token)
    #print(currently_playing_response)
    #print(currently_playing_response.json())

    playback_status_return = {}

    if currently_playing_response.status_code == 204:
        flash("there is no media currently playing")
        print("there is no media currently playing")
    elif currently_playing_response.status_code == 200:
        playback_status = currently_playing_response.json()
        if playback_status['item'] != None:
            playback_status_return['image'] = playback_status['item']['album']['images'][1]['url']
            playback_status_return['name'] = playback_status['item']['name']
            playback_status_return['id'] = playback_status['item']['id']
            playback_status_return['duration_ms'] = playback_status['item']['duration_ms']
            playback_status_return['progress_ms'] = playback_status['progress_ms']
        else:
            playback_status = {'good response, but empty item'}
    else: 
        playback_status_return = {'there was a bad status code on playback status'}

    return render_template('music_player.html', playback_status=playback_status_return)

@main.route('/get_live_player_info', methods=['GET', 'POST'])
def get_live_player_info():

    # set spotify_access_token and spotify_expires_at

    # "access_token" will only be in session if user is logged in
    if 'spotify_access_token' not in session:
        user = db.session.query(User).filter(User.id == session['user_id']).first()
        session['spotify_access_token'] = user.spotify_access_token
    if 'spotify_expires_at' not in session:
        user = db.session.query(User).filter(User.id == session['user_id']).first()
        session['spotify_expires_at'] = user.spotify_expires_at
    print("WENT PAST 2 IF STATEMENTS IN GET_LIVE_PLAYER_INFO")


    spotify_access_token = session['spotify_access_token']
    spotify_expires_at = session['spotify_expires_at']

    # force user to login if not logged in
    if spotify_access_token == None:
        return redirect(url_for('spotify_login', show_dialog=False))

    # if token is expired, we will refresh it in the background (user will not need to login again)
    if datetime.datetime.now().timestamp() > spotify_expires_at:
        print('token expired, refreshing.......')
        return redirect(url_for('main.spotify_refresh_token'))

    # makes rrequest to spotify api
    print(f'access token BEFORE currenrlt_oplayinh call:::: {spotify_access_token}')
    currently_playing_response = get_current_track_info(spotify_access_token)
    print(f' CURREPTLY PLAYING RESPONSE :::: {currently_playing_response}')
    if currently_playing_response.status_code == 200:
        return jsonify(currently_playing_response.json())
    if currently_playing_response.status_code == 204:
        return jsonify({})
    else:
        return jsonify({0:0})

@main.route('/pause_player', methods=['GET', 'POST'])
def pause_player():
    device_id = request.args.get('device_id', None)
    spotify_access_token = session['spotify_access_token']

    print(device_id)
    if device_id:
        pause_response = put_pause(spotify_access_token=spotify_access_token, device_id=device_id)
        if pause_response.status_code == 200:
            return jsonify({'status_code_from_pause_player': 200})
        else:
            print(pause_response)
            return pause_response
    else:
        print('no user id was passed')

@main.route('/play_player', methods=['GET', 'POST'])
def play_player():
    device_id = request.args.get('device_id', None)
    spotify_access_token = session['spotify_access_token']

    print('PLAYPLAYER API RESPOOOOOOOOOOOO')
    print(device_id)
    if device_id:
        play_response = put_play(spotify_access_token=spotify_access_token, device_id=device_id)
        print(f'resulting play_response: {play_response}')
        if play_response.status_code == 200:
            return jsonify({'status_code_from_playu_player': 200})
        else:
            print(play_response)
            return play_response
    else:
        print('no user id was passed')


@main.route('/spotify_player_obtain_comments',  methods=['GET', 'POST'])
def spotify_player_obtain_comments():
    given_timestamp = request.args.get('timestamp', None)
    media_id = request.args.get('media_id', None)
    #user = User.query.filter_by(id=session['user_id']).first()
    print()
    print(f'timestamp={given_timestamp}')
    print(f'timestamp={media_id}')
    comments = Comment.query.join(Media).filter(Media.id == media_id, Comment.timestamp <= int(given_timestamp), Comment.timestamp >= int(given_timestamp)-10).all()
    print(comments)
    comment_data = [{'username': comment.user.username, 
                     'text': comment.text,
                     'timestamp': comment.timestamp} 
                     for comment in comments]

    return jsonify(comment_data)


@main.route('/spotify_refresh_token')
def spotify_refresh_token():
    user = db.session.query(User).filter(User.id == session['user_id']).first()

    if user.spotify_refresh_token == None:
        return redirect(url_for('spotify_login', show_dialog=False))
    
    response = token_refresh_result(user.spotify_refresh_token)
    new_token_info = response.json()

    # REPLACE TO DATABSE CALL
    user.spotify_access_token = new_token_info['access_token']  # used to do tasks requiring auth (lasts a day)
    user.spotify_expires_at = datetime.datetime.now().timestamp() + new_token_info['expires_in']  # keeping track of when token expires
    db.session.commit()
    session['spotify_access_token'] = user.spotify_access_token
    session['spotify_expires_at'] = user.spotify_expires_at

    print(f'REAL NEW EXPIRES AT:{ datetime.datetime.now().timestamp() + new_token_info["expires_in"]}')

    return redirect(url_for('main.music_search'))













@main.route('/movies', methods=['GET'])
def movies_search():
    query = request.args.get('q', '')
    if query:
        movies = search_movies(query)
    else:
        movies = fetch_discover_movies()
    
    return render_template('movies_search.html', movies=movies, search_query=query)

@main.route('/movie/<int:movie_id>')
def movie(movie_id):
    movie = fetch_movie_details(movie_id=movie_id)
    if 'status_code' in movie and movie['status_code'] == 34:
        return redirect(url_for('main.movies_search'))

    user_rating = 0.0
    if 'user_id' in session:
        user_id = session.get('user_id')
        rating = db.session.query(Rating).join(Media).filter(Rating.user_id == user_id, Media.id == movie_id).first()
        if rating:
            user_rating = rating.rating

    return render_template('movie.html', movie=movie, user_rating=user_rating)


@main.route('/submit_review', methods=['POST'])
def submit_review():    
    # define variables from url params
    media_title  = request.args.get('media_title', None)
    media_id = request.args.get('media_id', None)
    media_type  = request.args.get('media_type', None)

     # check if user is signed in
    if 'user_id' not in session:
        return redirect(url_for('main.login'))

    # obtain neccesary vars from session and form 
    user_id = session['user_id']
    rating_given = request.form.get('rating')

    # define user and media var (note, if media is not found, it will default to NONE)
    user = db.session.query(User).filter(User.id == user_id).first()
    media = db.session.query(Media).filter(Media.id == media_id).first()
    rating = db.session.query(Rating).join(Media).filter(Rating.user_id == user_id, Media.id == media_id).first()

    # create a media object if none is found
    if not media:
        media = Media(id=media_id, title=media_title, media_type=media_type)
        db.session.add(media)
        db.session.commit()

    # add rating if not present, and update if alr presnet
    if user and media:
        if not rating:
            new_rating = Rating(user_id=user.id, media_id=media.unique_id, rating=rating_given)
            db.session.add(new_rating)
            print("CREATED NEW RATING")
        if rating:
            rating.rating = rating_given
            print("UPDATED RATING")
        db.session.commit()
    print(media_type)
    if media_type == 'movie':
        return redirect(url_for('main.movie', movie_id=media_id))
    if media_type == 'music':
        return redirect(url_for('main.song_detail', song_id=media_id))
    if media_type == 'show':
        return redirect(url_for('main.episode_details', episode_id=media_id))
    else:
        # Handle other media types (if applicable)
        return redirect(url_for('main.index'))
    
    # Process the rating (e.g., save it to the database)
    #flash('Thank you for your review!', 'success')
    #return redirect(url_for('main.movie', movie_id=movie_id))

@main.route('/submit_review_show', methods=['POST'])
def submit_review_show():

    # define variables from url params
    media_title  = request.args.get('media_title', None)
    media_id = request.args.get('media_id', None)
    print(media_id)
    media_type  = request.args.get('media_type', None)
    episode_title = request.args.get('episode_title', None)
    season_number=request.args.get('season_number', None) 
    episode_number=request.args.get('episode_number', None)

    # obtain neccesary vars from session and form 
    user_id = session['user_id']
    rating_given = request.form.get('rating')

    print(f'userid = {user_id}')

    # check if user is signed in
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    episode = db.session.query(Media).filter(Media.id == media_id, Media.season_number == season_number, Media.episode_number == episode_number).first()
    print(episode)
    rating = db.session.query(Rating).join(Media).filter(Rating.user_id == user_id, Media.id == media_id, Rating.season_number == season_number, Rating.episode_number == episode_number).first()
    print(rating)

    #  # create a media object if none is found
    # if not media:
    #     media = Media(id=media_id, title=media_title, media_type=media_type)
 
    # if current episode doesnt exist, add it to 
    if not episode:
        episode = Media(id=media_id, title=media_title, media_type=media_type, season_number=season_number, episode_number=episode_number, episode_title=episode_title)
        db.session.add(episode)
        db.session.commit()
    
    
    # add rating if not present, and update if alr presnet
    if not rating:
        new_rating = Rating(user_id=user_id, media_id=episode.unique_id, rating=rating_given, season_number=season_number, episode_number=episode_number )
        db.session.add(new_rating)
        print("CREATED NEW RATING")
    if rating:
        rating.rating = rating_given
        print("UPDATED RATING")
    db.session.commit()

    return redirect(url_for('main.episode_details', show_id=int(media_id), season_number=season_number, episode_number=episode_number))


@main.route('/submit_comment_show', methods=['POST'])
def submit_comment_show():

    # define variables from url params
    media_title  = request.args.get('media_title', None)
    media_id = request.args.get('media_id', None) # id of the show
    media_type  = request.args.get('media_type', None)
    episode_title = request.args.get('episode_title', None)
    season_number=request.args.get('season_number', None) 
    episode_number=request.args.get('episode_number', None)

    # obtain neccesary vars from session and form 
    user_id = session['user_id']
    timestamp = request.form.get('timestamp')
    text = request.form.get('text')

    # check if user is signed in
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    episode = db.session.query(Media).filter(Comment.user_id == user_id, Media.id == media_id, Media.episode_number == int(episode_number), Media.season_number == int(season_number)).first()
    print(episode)
    #comment = db.session.query(Comment).filter(Comment.user_id == user_id, Rating.media_id == media_id, Rating.season_number == season_number, Rating.episode_number == episode_number).first()

    #  # create a media object if none is found
    # if not media:
    #     media = Media(id=media_id, title=media_title, media_type=media_type)
 
    # if current episode doesnt exist, add it to 
    if not episode:
        episode = Media(id=media_id, title=media_title, media_type=media_type, season_number=int(season_number), episode_number=int(episode_number), episode_title=episode_title)
        db.session.add(episode)
        db.session.commit()

    print("faoejfoajeofjaefjaeof")
    print(timestamp)
    print(episode.id)
    print(episode.season_number)
    print(episode.episode_number)

    # add rating if not present, and update if alr presnet
    new_comment = Comment(user_id=user_id, media_id=episode.unique_id, timestamp=int(timestamp), text=text, season_number=season_number, episode_number=episode_number )
    db.session.add(new_comment)
    db.session.commit()


    return redirect(url_for('main.episode_details', show_id=int(media_id), season_number=season_number, episode_number=episode_number))


@main.route('/song/<song_id>')
def song_detail(song_id):
    song = get_track_info(song_id) #db.get_song_by_id(song_id)
    if 'status_code' in song and song['status_code'] == 34:
        return redirect(url_for('main.music_search'))

    user_rating = 0.0
    if 'user_id' in session:
        user_id = session.get('user_id')
        rating = db.session.query(Rating).join(Media).filter(Rating.user_id == user_id, Media.id == song_id).first()
        if rating:
            user_rating = rating.rating
            print(user_rating)

    return render_template('song.html', song=song, user_rating=user_rating)

@main.route('/shows', methods=['GET'])
def shows_search():
    query = request.args.get('q', '')
    if query:
        shows = search_tv_shows(query)
    else:
        shows = get_popular_tv_shows()
    
    return render_template('shows_search.html', shows=shows, search_query=query)

@main.route('/show/<int:show_id>')
def show_details(show_id):
    show_data = get_tv_show_details(show_id)
    show = {
        'id': show_data['id'],
        'title': show_data['name'],
        'poster_url': f"https://image.tmdb.org/t/p/w500{show_data['poster_path']}" if show_data['poster_path'] else None,
        'info': show_data['overview'],
        'seasons': [
            {
                'season_number': season['season_number'],
                'name': season['name'],
                'episodes': fetch_season_episodes(show_id, season['season_number'])
            }
            for season in show_data['seasons']
        ]
    }
    return render_template('show.html', show=show)

@main.route('/show/<int:show_id>/season/<int:season_number>/episode/<int:episode_number>')
def episode_details(show_id, season_number, episode_number):
    poster_url = fetch_show_poster(show_id, season_number)
    episode = fetch_episode_details(show_id, season_number, episode_number)
    show_data = get_tv_show_details(show_id)
    if 'status_code' in episode and episode['status_code'] == 34:
        return redirect(url_for('main.show_search'))
    
    show = {
        'id': show_data['id'],
        'title': show_data['name']
    }

    user_rating = 0.0
    if 'user_id' in session:
        user_id = session.get('user_id')
        rating = db.session.query(Rating).join(Media).filter(Rating.user_id == user_id, Media.id == show_id, Rating.season_number == season_number, Rating.episode_number == episode_number).first()
        if rating:
            user_rating = rating.rating
        
    return render_template('episode.html', episode=episode, show_id=show_id, episode_number=episode_number, season_number=season_number, poster_url=poster_url, show=show, user_rating=user_rating)

@main.route('/login', methods=['GET', 'POST'])
def login():
    global USER_ID

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            print()
            session['user_id'] = user.id  # Use 'user_id' to store user identifier
            print(f"current session user id : {session['user_id']}")
            USER_ID = user.id
            flash('Login successful!', 'success')
            print('Login successful!', 'success')
            return redirect(url_for('main.home'))
        else:
            print('Invalid username or password', 'danger')
            flash('Invalid username or password', 'danger')

    return render_template('login.html')


@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
        elif User.query.filter_by(email=email).first():
            flash('Email already exists', 'danger')
        else:
            new_user = User(username=username, password=generate_password_hash(password), email=email)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('main.login'))

    return render_template('register.html')

@main.route('/logout')
def logout():
    global USER_ID

    session.pop('username', None)
    session.pop('user_id', None)
    USER_ID = None

    flash('You have been logged out', 'success')
    return redirect(url_for('main.home'))

@main.route('/comments', methods=['GET'])
def get_comments():
    media_id = request.args.get('media_id')
    timestamp = int(request.args.get('timestamp'))
    print(timestamp)
    media_type = request.args.get('media_type')
    print(f'media_id:::{media_id}')
    print(db.session.query(Comment).all())
    comments = db.session.query(Comment).join(Media).filter(Media.id == media_id, Comment.timestamp == int(timestamp)).all()
    comment_data = [{'username': comment.user.username, 'text': comment.text, 'user_id': comment.user.id} for comment in comments]


    return jsonify(comment_data)

@main.route('/comments_show', methods=['GET'])
def get_comments_show():
    media_id = request.args.get('media_id')
    timestamp = int(request.args.get('timestamp'))
    #media_type = request.args.get('media_type')
    season_number = request.args.get('season_number')
    episode_number = request.args.get('episode_number')

    print("#2")
    print(timestamp)
    #print(unique_id)
    #print(media_title)
    print(media_id)
    #print(media_type)
    print(season_number)
    print(episode_number)
    #print(episode_title)

    comments = db.session.query(Comment).join(Media).filter(Media.id == media_id, Comment.season_number == int(season_number), Comment.episode_number == int(episode_number), Comment.timestamp == timestamp).all()
    print(comments)
    comment_data = [{'username': comment.user.username, 'text': comment.text, 'user_id': comment.user.id} for comment in comments]

    return jsonify(comment_data)



@main.route('/submit_comment', methods=['POST'])
def submit_comment():
    # Retrieve necessary variables from form or URL parameters
    media_title = request.args.get('media_title', None)
    media_id = request.args.get('media_id', None) # this goes in Media.id variable
    media_type = request.args.get('media_type', None)

    # Check if user is signed in (session check)
    if 'user_id' not in session:
        return redirect(url_for('main.login'))  # Redirect to login page if user is not logged in

    # Obtain necessary variables from session and form
    user_id = session['user_id']
    timestamp = request.form.get('timestamp')
    text = request.form.get('text')

    # Find the user and media objects (create media if not found)
    user = db.session.query(User).filter(User.id == user_id).first()
    media = db.session.query(Media).filter(Media.id == media_id).first()
    print(media)

    if not media:
        # Create a new media object if not found
        print('media created')
        media = Media(id=media_id, title=media_title, media_type=media_type)
        db.session.add(media)
        db.session.commit()

    # Create a new comment object and associate it with the user and media
    if user and media:
        new_comment = Comment(user_id=user.id, media_id=media.unique_id, timestamp=int(timestamp), text=text)
        db.session.add(new_comment)
        db.session.commit()

        # Redirect to a success page or return a JSON response indicating success
        return jsonify({'message': 'Comment submitted successfully'})

    # Handle error or invalid request
    return jsonify({'error': 'Failed to submit comment'}), 400  # Return a JSON error response with status code 400






@main.route('/submit_comment_live_player', methods=['GET', 'POST'])
def submit_comment_live_player():
    # Retrieve necessary variables from form or URL parameters
    media_title = request.args.get('media_title', None)
    media_id = request.args.get('media_id', None) # this goes in Media.id variable
    media_type = request.args.get('media_type', None)
    timestamp = request.args.get('timestamp', None)
    text = request.args.get('text', None)

    # Check if user is signed in (session check)
    if 'user_id' not in session:
        return redirect(url_for('main.login'))  # Redirect to login page if user is not logged in

    # Obtain necessary variables from session 
    user_id = session['user_id']

    # Find the user and media objects (create media if not found)
    user = db.session.query(User).filter(User.id == user_id).first()
    media = db.session.query(Media).filter(Media.id == media_id).first()
    print(media)

    if not media:
        # Create a new media object if not found
        print('media created')
        media = Media(id=media_id, title=media_title, media_type=media_type)
        db.session.add(media)
        db.session.commit()

    # Create a new comment object and associate it with the user and media
    if user and media:
        new_comment = Comment(user_id=user.id, media_id=media.unique_id, timestamp=int(timestamp), text=text)
        db.session.add(new_comment)
        db.session.commit()

        # Redirect to a success page or return a JSON response indicating success
        return jsonify({'message': 'Comment submitted successfully'})

    # Handle error or invalid request
    return jsonify({'error': 'Failed to submit comment'}), 400  # Return a JSON error response with status code 400




@main.route('/account')
def account():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    ratings = Rating.query.filter_by(user_id=user_id).all()
    
    # Get all comments by the user
    comments = Comment.query.filter_by(user_id=user_id).all()

    # Organize ratings by media title and season/episode
    ratings_by_media = defaultdict(lambda: defaultdict(list))
    for rating in ratings:
        media_title = rating.media.title
        if rating.media.season_number and rating.media.episode_number:
            season_episode = f"Season {rating.media.season_number} Episode {rating.media.episode_number}: {rating.media.episode_title}"
        else:
            season_episode = None
        ratings_by_media[media_title][season_episode].append(rating.rating)

    # Group comments by media title
    comments_by_media = {}
    for comment in comments:
        media_title = comment.media.title
        if media_title not in comments_by_media:
            comments_by_media[media_title] = []
        comments_by_media[media_title].append(comment)

    # Define media type function
    def get_media_type(title):
        media = Media.query.filter_by(title=title).first()
        if media:
            return media.media_type  # Assuming 'type' is a field in Media model
        return 'unknown'

    
    def get_media_id(title):
        media = Media.query.filter_by(title=title).first()
        if media:
            return media.id  # Assuming 'type' is a field in Media model
        return 'unknown'

    return render_template(
        'account.html',
        user=user,
        ratings_by_media=ratings_by_media,
        comments_by_media=comments_by_media,
        media_type=get_media_type,
        media_id=get_media_id
    )


@main.record_once
def register_template_filters(state):
    app = state.app
    @app.template_filter('timestamp_to_hms')
    def timestamp_to_hms_filter(seconds):
        if seconds is None or not isinstance(seconds, (int, float)):
            return 'N/A'  # or any other default value you prefer
        return str(timedelta(seconds=int(seconds)))


@main.route('/user/<int:user_id>')
def user_profile(user_id):
    user = User.query.get(user_id)
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('main.home'))

    comments = Comment.query.filter_by(user_id=user_id).all()
    ratings = Rating.query.filter_by(user_id=user_id).all()

    # Organize ratings by media title and season/episode
    ratings_by_media = defaultdict(lambda: defaultdict(list))
    for rating in ratings:
        media_title = rating.media.title
        if rating.media.season_number and rating.media.episode_number:
            season_episode = f"Season {rating.media.season_number} Episode {rating.media.episode_number}: {rating.media.episode_title}"
        else:
            season_episode = None
        ratings_by_media[media_title][season_episode].append(rating.rating)
    
    # Group comments by media title
    comments_by_media = {}
    for comment in comments:
        media_title = comment.media.title
        if media_title not in comments_by_media:
            comments_by_media[media_title] = []
        comments_by_media[media_title].append(comment)

    # Define media type function
    def get_media_type(title):
        media = Media.query.filter_by(title=title).first()
        if media:
            return media.media_type  # Assuming 'type' is a field in Media model
        return 'unknown'

    def get_media_id(title):
        media = Media.query.filter_by(title=title).first()
        if media:
            return media.id  # Assuming 'type' is a field in Media model
        return 'unknown'


    return render_template(
        'user_profile.html',
        user=user,
        comments_by_media=comments_by_media,
        ratings_by_media=ratings_by_media,
        media_type=get_media_type,
        media_id=get_media_id
    )

