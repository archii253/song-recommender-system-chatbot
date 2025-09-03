import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Last.fm API
    LASTFM_API_KEY = os.getenv('LASTFM_API_KEY')
    LASTFM_API_SECRET = os.getenv('LASTFM_API_SECRET')
    LASTFM_BASE_URL = 'http://ws.audioscrobbler.com/2.0/'
    
    # YouTube API
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
    YOUTUBE_BASE_URL = 'https://www.googleapis.com/youtube/v3/'
    
    # Database
    DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///database/recommendations.db')
    
    # Model paths
    SIMILARITY_MODEL_PATH = 'ml_models/similarity_model.pkl'
    NLP_MODEL_PATH = 'ml_models/nlp_model.h5'
    
    # Recommendation settings
    MAX_RECOMMENDATIONS = 5
    MAX_CHAT_HISTORY = 10