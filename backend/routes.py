from backend.movie_api import fetch_movies, search_movies, fetch_discover_movies, fetch_movie_details
from flask import Blueprint, request, render_template, flash,  session, url_for, redirect, Flask, jsonify
from backend.database import db
from backend.tv_show_api import get_popular_tv_shows_for_carousel
from backend.music_api import get_home_tracks, get_search_tracks, get_track_info
from backend.search_form import SearchForm
from werkzeug.security import generate_password_hash, check_password_hash
from backend.models import User, Comment, Rating, Media
from backend.tv_show_api import search_tv_shows

import json


main = Blueprint('main', __name__)

@main.route('/')
def home():
    movies = fetch_movies()
    if not movies:
        return "Failed to fetch movies. Please try again later.", 500
    tracks = get_home_tracks()
    shows = get_popular_tv_shows_for_carousel()
    return render_template('home.html', movies=movies, tracks=tracks, shows=shows)


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
    
    return render_template('movie.html', movie=movie)

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
    rating = db.session.query(Rating).filter(Rating.user_id == user_id, Rating.media_id == media_id).first()

    # create a media object if none is found
    if not media:
        media = Media(id=media_id, title=media_title, media_type=media_type)

    # add rating if not present, and update if alr presnet
    if user and media:
        if not rating:
            new_rating = Rating(user_id=user.id, media_id=media.id, rating=rating_given)
            db.session.add(new_rating)
            print("CREATED NEW RATING")
        if rating:
            rating.rating = rating_given
            print("UPDATED RATING")
        db.session.commit()

    if media_type == 'movie':
        return redirect(url_for('main.movie', movie_id=media_id))
    if media_type == 'music':
        return redirect(url_for('main.song_detail', song_id=media_id))
    if media_type == 'show':
        return redirect(url_for('main.show', movie_id=media_id))
    
    # Process the rating (e.g., save it to the database)
    #flash('Thank you for your review!', 'success')
    #return redirect(url_for('main.movie', movie_id=movie_id))

from flask import request, jsonify

# @main.route('/comments', methods=['GET'])
# def get_comments():
#     movie_id = request.args.get('movie_id')
#     timestamp = int(request.args.get('timestamp', 0))
#     comments = Comment.query.filter_by(movie_id=movie_id, timestamp=timestamp).all()
#     comments_data = [{'timestamp': c.timestamp, 'text': c.text} for c in comments]
#     return jsonify(comments_data)

# @main.route('/submit_comment', methods=['POST'])
# def submit_comment():
#     data = request.get_json()
#     movie_id = data['movie_id']
#     text = data['text']
#     timestamp = data['timestamp']
#     new_comment = Comment(movie_id=movie_id, text=text, timestamp=timestamp)
#     db.session.add(new_comment)
#     db.session.commit()
#     return jsonify({'success': True})

@main.route('/music', methods=['GET','POST'])
def music_search():
    form = SearchForm()
    results = []

    if form.validate_on_submit():
        results = get_search_tracks( form.name_search.data )
        if len(results) == 1 and results[0] == False:
            results = 'Result Not Found'
        print("$####################")
        print(results[0])
    else:
        results = get_home_tracks()
        
    return render_template('music_search.html', results=results, form=form)

@main.route('/song/<song_id>')
def song_detail(song_id):
    # Retrieve song details, comments, and other relevant data from the database
    song = get_track_info(song_id) #db.get_song_by_id(song_id)
    #comments = db.get_comments_for_song(song_id)

    # this is a placeholder for now, until we design the db 
    # comments = [{'username': 'egger',
    #              'text': 'when he said "so many racks they call me the bandman" i felt that',
    #              'timestamp': '5:55'
    #             },
    #             {'username': 'second user',
    #              'text': 'wowzers',
    #              'timestamp': '1:01'
    #             }]
    print(song['artists'])
    return render_template('song.html', song=song)

@main.route('/shows')
@main.route('/shows', methods=['GET','POST'])
def shows_search():
    form = SearchForm()
    results = []

    if form.validate_on_submit():
        query = form.name_search.data
        results = search_tv_shows(query)
        print("$####################")
        if results:
            print(results[0])
        else:
            print("No results found")

    return render_template('shows_search.html', results=results, form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id  # Use 'user_id' to store user identifier
            flash('Login successful!', 'success')
            return redirect(url_for('main.home'))
        else:
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
        else:
            new_user = User(username=username, password=generate_password_hash(password), email=email)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('main.login'))

    return render_template('register.html')

@main.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('main.login'))

@main.route('/comments', methods=['GET'])
def get_comments():
    media_id = request.args.get('media_id')
    timestamp = int(request.args.get('timestamp'))
    media_type = request.args.get('media_type')

    comments = db.session.query(Comment).filter(Comment.media_id == media_id, Comment.timestamp == timestamp).all()

    comment_data = [{'username': comment.user.username, 'text': comment.text} for comment in comments]
    #print(comment_data)
    return jsonify(comment_data)

@main.route('/submit_comment', methods=['POST'])
def submit_comment():
    # define neccesary vars from url params
    media_title  = request.args.get('media_title', None)
    media_id = request.args.get('media_id', None)
    media_type  = request.args.get('media_type', None)

    # check if user is signed in
    if 'user_id' not in session:
        return redirect(url_for('main.login'))

    # obtain neccesary vars from session and form 
    user_id = session['user_id']
    #media_id = request.form.get('media_id')
    timestamp = request.form.get('timestamp')
    text = request.form.get('text')

    # define user and media var (note, if media is not found, it will default to NONE)
    user = db.session.query(User).filter(User.id == user_id).first()
    media = db.session.query(Media).filter(Media.id == media_id).first()

    # create a media object if none is found
    if not media:
        media = Media(id=media_id, title=media_title, media_type=media_type)

    # add comment, and assign it a user
    if user and media:
        new_comment = Comment(user_id=user.id, media_id=media.id, timestamp=int(timestamp), text=text)
        db.session.add(new_comment)
        db.session.commit()

@main.route('/account')
def account():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))

    user_id = session['user_id']
    user = db.session.query(User).filter(User.id == user_id).first()
    comments = db.session.query(Comment).filter(Comment.user_id == user_id).all()
    ratings = db.session.query(Rating).filter(Rating.user_id == user_id).all()

    return render_template('account.html', user=user, comments=comments, ratings=ratings)


