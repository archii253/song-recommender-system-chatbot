from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    interactions = db.relationship('UserInteraction', backref='user', lazy=True)

class UserInteraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    input_text = db.Column(db.String(500), nullable=False)
    response = db.Column(db.String(1000), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    feedback = db.Column(db.Integer)  # 1=positive, 0=negative, None=no feedback

class RecommendedTrack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    interaction_id = db.Column(db.Integer, db.ForeignKey('user_interaction.id'), nullable=False)
    track_name = db.Column(db.String(200), nullable=False)
    artist = db.Column(db.String(200), nullable=False)
    youtube_link = db.Column(db.String(500))
    similarity_score = db.Column(db.Float)

    interaction = db.relationship('UserInteraction', backref='recommended_tracks')