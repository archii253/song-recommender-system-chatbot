from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, User, UserInteraction, RecommendedTrack
from recommender import SongRecommender
from config import Config
import uuid

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

recommender = SongRecommender()

# Create tables
with app.app_context():
    db.create_all()

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_id = data.get('user_id', str(uuid.uuid4()))  # Create new user if not provided
        message = data.get('message', '')
        chat_history = data.get('chat_history', [])
        
        # Get or create user
        user = User.query.filter_by(username=user_id).first()
        if not user:
            user = User(username=user_id)
            db.session.add(user)
            db.session.commit()
        
        # Get recommendations
        if chat_history:
            recommendations = recommender.recommend_based_on_history(chat_history)
        else:
            recommendations = recommender.recommend_based_on_text(message)
        
        # Format response
        response_text = generate_response_text(recommendations)
        response = {
            "recommendations": recommendations[:Config.MAX_RECOMMENDATIONS],
            "response_text": response_text
        }
        
        # Store interaction
        interaction = UserInteraction(
            user_id=user.id,
            input_text=message,
            response=response_text
        )
        db.session.add(interaction)
        db.session.commit()  # commit to get interaction.id
        
        # Store recommendations
        for rec in recommendations[:Config.MAX_RECOMMENDATIONS]:
            db.session.add(RecommendedTrack(
                interaction_id=interaction.id,
                track_name=rec['track'],
                artist=rec['artist'],
                youtube_link=rec['youtube_link'],
                similarity_score=rec['similarity_score']
            ))
        
        db.session.commit()
        
        return jsonify({
            'user_id': user_id,
            'response': response,
            'chat_id': interaction.id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

def generate_response_text(recommendations):
    if not recommendations:
        return "I couldn't find any recommendations based on your input. Could you provide more details?"
    
    top_rec = recommendations[0]
    artist = top_rec['artist']
    track = top_rec['track']
    
    if len(recommendations) == 1:
        return f"I recommend '{track}' by {artist}. Would you like to hear more about this track?"
    else:
        return f"Based on your preferences, I recommend '{track}' by {artist}. I also have some other suggestions you might like."

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)