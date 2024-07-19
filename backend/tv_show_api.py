import requests
from backend.config import Config


def get_tv_show_details(tv_show_id):
    url = f"https://api.themoviedb.org/3/tv/{tv_show_id}"
    params = {'api_key': Config.TV_API_KEY}
    response = requests.get(url, params=params)
    return response.json()


def search_tv_shows(query):
    url = "https://api.themoviedb.org/3/search/tv"
    params = {'api_key': Config.TV_API_KEY, 'query': query}
    response = requests.get(url, params=params)
    return response.json().get('results', [])


def get_popular_tv_shows():
    url = "https://api.themoviedb.org/3/tv/popular?language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {Config.TV_ACCESS_TOKEN}"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        return []
