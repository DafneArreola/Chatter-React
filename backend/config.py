import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MOVIE_API_KEY = os.environ.get('MOVIE_API_KEY')
    MOVIE_ACCESS_TOKEN = os.environ.get('MOVIE_ACCESS_TOKEN')

    MUSIC_CLIENT_ID = '1a9bd2df8c6c44afbbf527403e7306e3'
    MUSIC_CLIENT_SECRET = 'edb1c825d83f4719b733d3b8ed05a4e9'


