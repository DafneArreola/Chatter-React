import requests
from backend.config import Config
import logging

API_KEY = Config.TV_API_KEY

logging.basicConfig(level=logging.DEBUG)

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


def get_popular_tv_shows_for_carousel():
    url = "https://api.themoviedb.org/3/tv/popular?language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {Config.TV_ACCESS_TOKEN}"
    }

    response = requests.get(url, headers=headers)
    shows = response.json().get('results', [])

    filtered_shows = []
    for show in shows[:18]:  # Limiting to the first 18 popular shows for the carousel
        new_entry = {
            'name': show['name'],
            'image': show['poster_path'] and f"https://image.tmdb.org/t/p/w500{show['poster_path']}"
        }
        filtered_shows.append(new_entry)
    # print("Filtered Shows: ", filtered_shows)  # Debugging
    return filtered_shows



def fetch_shows():
    url = f'https://api.themoviedb.org/3/tv/popular?api_key={API_KEY}&language=en-US&page=1'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data:
            shows = data['results'][:18]
            return shows
        else:
            logging.error(f"Unexpected response structure: {data}")
            return []
    else:
        logging.error(f"Failed to fetch shows: {response.status_code}")
        return []

def fetch_discover_shows():
    url = f'https://api.themoviedb.org/3/discover/tv?include_adult=false&include_null_first_air_dates=false&language=en-US&page=1&sort_by=popularity.desc&api_key={API_KEY}'
    response = requests.get(url)
    data = response.json()
    if 'results' in data:
        shows = data['results'][:20] 
        return shows
    else:
        logging.error(f"Unexpected response structure: {data}")
        return []

def search_shows(query):
    url = f'https://api.themoviedb.org/3/search/tv?query={query}&include_adult=false&language=en-US&page=1&api_key={API_KEY}'
    response = requests.get(url)
    data = response.json()
    if 'results' in data:
        shows = data['results']
        return shows
    else:
        logging.error(f"Unexpected response structure: {data}")
        return []


def fetch_show_details(show_id, season_number):
    url = f'https://api.themoviedb.org/3/tv/{show_id}/season/{season_number}?api_key={API_KEY}&language=en-US'
    
    response = requests.get(url)
    show = response.json()
    return show

def fetch_episode_details(show_id, season_number, episode_number):
    url = f'https://api.themoviedb.org/3/tv/{show_id}/season/{season_number}/episode/{episode_number}?api_key={API_KEY}&language=en-US'
    
    response = requests.get(url)
    show = response.json()
    return show

def fetch_season_episodes(show_id, season_number):
    # Fetch details for a specific season
    season_data = fetch_show_details(show_id, season_number)
    episodes = [
        {
            'number': episode['episode_number'],
            'title': episode['name']
        }
        for episode in season_data['episodes']
    ]
    return episodes

def fetch_show_poster(show_id, season_number):
    """
    Fetch the poster URL for a TV show given its ID.
    :param show_id: The ID of the TV show.
    :return: The URL of the show's poster.
    """
    data = fetch_show_details(show_id, season_number)
    poster_path = data.get('poster_path')
    return poster_path
