from flask import Blueprint, request, render_template, flash, session, url_for, redirect, Flask
from backend.database import db
from backend.movie_api import get_movie_details, search_movies, get_popular_movies
from backend.music_api import get_home_tracks
from werkzeug.security import generate_password_hash, check_password_hash
from backend.models import User

main = Blueprint('main', __name__)

@main.route('/')
def home():
    movies = get_popular_movies()
    tracks = get_home_tracks()
    return render_template('home.html', movies=movies, tracks=tracks)

@main.route('/movies')
def movies():
    return render_template('movies.html', movies=movies)

@main.route('/music')
def music_search():
    return render_template('music_search.html')

# @main.route('/music_search', methods=['GET'])
# def music_search():
#     query = request.args.get('q', '')
#     results = search_songs(query)  # Replace with your actual search function
#     return render_template('music_search_results.html', query=query)

# @main.route('/song/<int:song_id>')
# def song_detail(song_id):
#     # Retrieve song details, comments, and other relevant data from the database
#     song = db.get_song_by_id(song_id)
#     comments = db.get_comments_for_song(song_id)
#     return render_template('song_detail.html', song=song, comments=comments)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
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
            return redirect(url_for('login'))

    return render_template('register.html')

# @main.route('/dashboard')
# def dashboard():
#     if 'username' not in session:
#         flash('Please login to access this page', 'danger')
#         return redirect(url_for('login'))

#     return f'Welcome to your dashboard, {session["username"]}!'

@main.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))
