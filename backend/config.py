import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY=os.environ.get('SECRET_KEY')
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    MOVIE_API_KEY = os.environ.get('MOVIE_API_KEY')
    MOVIE_ACCESS_TOKEN = os.environ.get('MOVIE_ACCESS_TOKEN')

    TV_API_KEY = os.getenv('TV_API_KEY')
    TV_ACCESS_TOKEN = os.getenv('TV_ACCESS_TOKEN')

    MUSIC_CLIENT_ID = '1a9bd2df8c6c44afbbf527403e7306e3'
    MUSIC_CLIENT_SECRET = 'edb1c825d83f4719b733d3b8ed05a4e9'





