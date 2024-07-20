from flask import Blueprint, request, render_template, flash
from backend.database import db
from backend.movie_api import get_movie_details, search_movies, get_popular_movies
from backend.music_api import get_home_tracks, get_search_tracks, get_track_info
from backend.search_form import SearchForm

main = Blueprint('main', __name__)


@main.route('/')
def home():
    movies = get_popular_movies()
    tracks = get_home_tracks()
    return render_template('home.html', movies=movies, tracks=tracks)

@main.route('/movies')
def movies():
    return render_template('movies.html', movies=movies)

@main.route('/music', methods=['GET','POST'])
def music_search():
    form = SearchForm()
    results = []

    if form.validate_on_submit():
        results = get_search_tracks( form.name_search.data )
        print("$####################")
        print(results[0])
        
    return render_template('music_search.html', results=results, form=form)

@main.route('/temp')
def temp():
    id = request.args.get('id', None)
    if id:
        song_info = get_track_info(id)
    else:
        song_id = None
    return render_template('temp.html', song_info=song_info)

@main.route('/song/<song_id>')
def song_detail(song_id):
    # Retrieve song details, comments, and other relevant data from the database
    song = get_track_info(song_id) #db.get_song_by_id(song_id)
    #comments = db.get_comments_for_song(song_id)

    # this is a placeholder for now, until we design the db 
    comments = [{'username': 'egger',
                 'text': 'when he said "so many racks they call me the bandman" i felt that',
                 'timestamp': '5:55'
                },
                {'username': 'second user',
                 'text': 'wowzers',
                 'timestamp': '1:01'
                }]
    print(song['artists'])
    return render_template('song.html', song=song, comments=comments)

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