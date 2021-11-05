'''Helpers such as API handling defs'''

import requests
from threading import Timer


API_KEY = 'f004f106763bbbfa038ef135fe7f4d1a46fc852f'
BASE_SEARCH_URL = 'https://www.giantbomb.com/api/search/'
BASE_GAME_URL = 'https://www.giantbomb.com/api/game/'
BASE_VIDEO_URL = 'https://www.giantbomb.com/api/video/'


def search_query(query_str):
    '''Accepts query string and makes the API call to get the initial search response.'''
    
    params = dict(
        api_key=API_KEY,
        format='json',
        query=query_str,
        resources='game'
    )
    
    headers = {"user-agent": "jGamesWebApp"}
    
    search_resp = requests.get(url=BASE_SEARCH_URL, params=params, headers=headers)
    
    return search_resp.json()


def game_query(query_str):
    '''Accepts a game's guid and makes an API call to get individual details.'''
    
    params = dict(
        api_key=API_KEY,
        format='json'
    )
    
    headers = {"user-agent": "jGamesWebApp"}
    
    game_resp = requests.get(url=f'{BASE_GAME_URL}{query_str}', params=params, headers=headers)
    
    return game_resp.json()


def video_query(query_str):
    '''Accepts an API video guid and makes the appropriate call for extracting embeded players.'''
    
    params = dict(
        api_key=API_KEY,
        format='json'
    )
    
    headers = {"user-agent": "jGamesWebApp"}
    
    video_resp = requests.get(url=f'{BASE_VIDEO_URL}{query_str}', params=params, headers=headers)
    
    return video_resp.json()