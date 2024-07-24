import requests
import logging
from backend.config import Config

API_KEY = Config.MOVIE_API_KEY

logging.basicConfig(level=logging.DEBUG)

def fetch_movies():
    url = f'https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=en-US&page=1'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data:
            movies = data['results'][:18]  # Get only the first 18 movies
            return movies
        else:
            logging.error(f"Unexpected response structure: {data}")
            return []
    else:
        logging.error(f"Failed to fetch movies: {response.status_code}")
        return []

def fetch_discover_movies():
    url = f'https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc&api_key={API_KEY}'
    response = requests.get(url)
    data = response.json()
    if 'results' in data:
        movies = data['results'][:20]  # Get only the first 18 movies
        return movies
    else:
        logging.error(f"Unexpected response structure: {data}")
        return []

def search_movies(query):
    url = f'https://api.themoviedb.org/3/search/movie?query={query}&include_adult=false&language=en-US&page=1&api_key={API_KEY}'
    response = requests.get(url)
    data = response.json()
    if 'results' in data:
        movies = data['results']
        return movies
    else:
        logging.error(f"Unexpected response structure: {data}")
        return []

def fetch_movie_details(movie_id):
    movie_id = int(movie_id)
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US'
    
    response = requests.get(url)
    movie = response.json()
    return movie
