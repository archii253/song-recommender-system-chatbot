import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from api_connectors import LastFMConnector, YouTubeConnector
from nlp_processor import NLPProcessor
from config import Config

class SongRecommender:
    def __init__(self):
        self.lastfm = LastFMConnector()
        self.youtube = YouTubeConnector()
        self.nlp = NLPProcessor()
        self.similarity_model = self.load_similarity_model()
    
    def load_similarity_model(self):
        try:
            with open(Config.SIMILARITY_MODEL_PATH, 'rb') as f:
                return pickle.load(f)
        except:
            return None
    
    def recommend_based_on_text(self, text):
        if not text or not isinstance(text, str):
            raise ValueError("Invalid input text")

        # Extract entities from user input
        entities = self.nlp.extract_entities(text)
        
        recommendations = []
        
        # If specific songs or artists are mentioned
        if entities['songs'] or entities['artists']:
            for song in entities['songs']:
                artist = entities['artists'][0] if entities['artists'] else ''
                similar_tracks = self.lastfm.get_similar_tracks(song, artist, Config.MAX_RECOMMENDATIONS)
                recommendations.extend(similar_tracks)
        
        # If no specific songs/artists, use semantic search
        else:
            # This would be enhanced with a proper music knowledge base
            popular_tracks = self.lastfm.search_tracks(text, Config.MAX_RECOMMENDATIONS)
            recommendations.extend(popular_tracks)
        
        # Process recommendations
        processed_recs = []
        for track in recommendations[:Config.MAX_RECOMMENDATIONS]:
            artist = track.get('artist', {}).get('name', 'Unknown Artist')
            track_name = track.get('name', 'Unknown Track')
            youtube_link = self.youtube.search_video(track_name, artist)
            
            processed_recs.append({
                'artist': artist,
                'track': track_name,
                'youtube_link': youtube_link,
                'similarity_score': self.nlp.calculate_similarity(text, f"{artist} {track_name}")
            })
        
        # Sort by similarity score
        processed_recs.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return processed_recs
    
    def recommend_based_on_history(self, chat_history):
        # Combine all chat messages
        combined_text = ' '.join([msg['content'] for msg in chat_history if msg['role'] == 'user'])
        
        # Get recommendations based on combined context
        return self.recommend_based_on_text(combined_text)
    
    def get_track_details(self, track, artist):
        lastfm_info = self.lastfm.get_track_info(track, artist)
        youtube_link = self.youtube.search_video(track, artist)
        
        return {
            'track': track,
            'artist': artist,
            'album': lastfm_info.get('album', {}).get('title', 'Unknown Album'),
            'duration': lastfm_info.get('duration', 0),
            'tags': [tag.get('name', '') for tag in lastfm_info.get('toptags', {}).get('tag', [])],
            'youtube_link': youtube_link,
            'summary': lastfm_info.get('wiki', {}).get('summary', '') if lastfm_info.get('wiki') else ''
        }