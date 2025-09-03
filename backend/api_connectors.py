import requests
import json
from config import Config

class LastFMConnector:
    def __init__(self):
        self.api_key = Config.LASTFM_API_KEY
        self.base_url = Config.LASTFM_BASE_URL
    
    def get_similar_tracks(self, track, artist, limit=5):
        params = {
            'method': 'track.getSimilar',
            'artist': artist,
            'track': track,
            'api_key': self.api_key,
            'format': 'json',
            'limit': limit
        }
        response = requests.get(self.base_url, params=params)
        return response.json().get('similartracks', {}).get('track', [])
    
    def get_track_info(self, track, artist):
        params = {
            'method': 'track.getInfo',
            'artist': artist,
            'track': track,
            'api_key': self.api_key,
            'format': 'json'
        }
        response = requests.get(self.base_url, params=params)
        return response.json().get('track', {})
    
    def search_tracks(self, query, limit=5):
        params = {
            'method': 'track.search',
            'track': query,
            'api_key': self.api_key,
            'format': 'json',
            'limit': limit
        }
        response = requests.get(self.base_url, params=params)
        return response.json().get('results', {}).get('trackmatches', {}).get('track', [])

class YouTubeConnector:
    def __init__(self):
        self.api_key = Config.YOUTUBE_API_KEY
        self.base_url = Config.YOUTUBE_BASE_URL
    
    def search_video(self, track, artist):
        query = f"{artist} - {track} official"
        params = {
            'part': 'snippet',
            'q': query,
            'type': 'video',
            'key': self.api_key,
            'maxResults': 1
        }
        response = requests.get(self.base_url + 'search', params=params)
        items = response.json().get('items', [])
        if items:
            return f"https://www.youtube.com/watch?v={items[0]['id']['videoId']}"
        return None
    
    def get_video_details(self, video_id):
        params = {
            'part': 'snippet,contentDetails',
            'id': video_id,
            'key': self.api_key
        }
        response = requests.get(self.base_url + 'videos', params=params)
        return response.json().get('items', [{}])[0]