import requests
from backend.config import Config

def get_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {'api_key': Config.MOVIE_API_KEY}
    response = requests.get(url, params=params)
    return response.json()

def search_movies(query):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {'api_key': Config.MOVIE_API_KEY, 'query': query}
    response = requests.get(url, params=params)
    return response.json().get('results', [])

def get_popular_movies():
    url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {Config.MOVIE_ACCESS_TOKEN}"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        return []