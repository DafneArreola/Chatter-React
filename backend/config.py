import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MOVIE_API_KEY = os.environ.get('MOVIE_API_KEY')
    MOVIE_ACCESS_TOKEN = os.environ.get('MOVIE_ACCESS_TOKEN')
