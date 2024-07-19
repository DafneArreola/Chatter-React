from flask import Blueprint, request, render_template
from backend.database import db

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html', movies=movies)

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