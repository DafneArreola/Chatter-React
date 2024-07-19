from flask import Blueprint, request, jsonify, render_template
from backend.database import db
from backend.movie_api import get_movie_details, search_movies, get_popular_movies


main = Blueprint('main', __name__)

@main.route('/')
def home():
    movies = get_popular_movies()
    return render_template('home.html', movies=movies)

