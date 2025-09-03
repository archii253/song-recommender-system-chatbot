from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, User, UserInteraction, RecommendedTrack
from recommender import SongRecommender
from config import Config
import uuid

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recommendations.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

recommender = SongRecommender()

# Create tables
with app.app_context():
    db.create_all()

@app.route('/api/track_details', methods=['GET'])
def track_details():
    track = request.args.get('track')
    artist = request.args.get('artist')
    
    if not track or not artist:
        return jsonify({'error': 'Track and artist parameters are required'}), 400
    
    details = recommender.get_track_details(track, artist)
    return jsonify(details)

@app.route('/api/feedback', methods=['POST'])
def feedback():
    data = request.json
    interaction_id = data.get('interaction_id')
    feedback_value = data.get('feedback')  # 1 for positive, 0 for negative
    
    if interaction_id is None or feedback_value is None:
        return jsonify({'error': 'interaction_id and feedback are required'}), 400
    
    interaction = UserInteraction.query.get(interaction_id)
    if not interaction:
        return jsonify({'error': 'Interaction not found'}), 404
    
    interaction.feedback = feedback_value
    db.session.commit()
    
    return jsonify({'status': 'success'})

def generate_response_text(self, recommendations):
    if not recommendations:
        return "I couldn't find any recommendations based on your input. Could you provide more details?"
    
    top_rec = recommendations[0]
    artist = top_rec['artist']
    track = top_rec['track']
    
    if len(recommendations) == 1:
        return f"I recommend '{track}' by {artist}. Would you like to hear more about this track?"
    else:
        return f"Based on your preferences, I recommend '{track}' by {artist}. I also have some other suggestions you might like."

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        if not data or 'message' not in data:
            return jsonify({"error": "Missing 'message' field"}), 400

        message = data.get('message', '')
        
        # Get recommendations
        recommender = SongRecommender()
        recommendations = recommender.recommend_based_on_text(message)
        
        # Log interaction to database
        interaction = UserInteraction(
            input_text=message,
            response=f"Found {len(recommendations)} recommendations",
            feedback=None  # Will be updated later if user gives feedback
        )
        db.session.add(interaction)
        db.session.commit()
        
        # Format recommendations
        formatted_recs = []
        for rec in recommendations:
            formatted_recs.append({
                'track': rec.get('track'),
                'artist': rec.get('artist'),
                'youtube_link': rec.get('youtube_link'),
                'similarity_score': rec.get('similarity_score')
            })
            # Log each recommendation to database
            db.session.add(RecommendedTrack(
                interaction_id=interaction.id,
                track_name=rec.get('track'),
                artist=rec.get('artist'),
                youtube_link=rec.get('youtube_link'),
                similarity_score=rec.get('similarity_score')
            ))
        
        db.session.commit()
        
        return jsonify({
            "response_text": interaction.response,
            "recommendations": formatted_recs,
            "chat_id": interaction.id  # For feedback tracking
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5000, debug=True)