# backend/models.py
from backend.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    comments = db.relationship('Comment', backref='user', lazy=True)
    ratings = db.relationship('Rating', backref='user', lazy=True)

    spotify_access_token = db.Column(db.String(500), nullable=True)
    spotify_refresh_token = db.Column(db.String(500), nullable=True)
    spotify_expires_at = db.Column(db.Float, nullable=True)

class Media(db.Model):
    unique_id = db.Column(db.Integer, primary_key=True, autoincrement=True) # this is the unique key for each row
    id = db.Column(db.String(50)) # this is the MEDIA_ID (it is possible that many show episodes have same "id")
    title = db.Column(db.String(255), nullable=False)
    media_type = db.Column(db.String(50), nullable=False)  # 'movie', 'show', 'track', etc.
    comments = db.relationship('Comment', backref='media', lazy=True)
    ratings = db.relationship('Rating', backref='media', lazy=True)

    episode_title = db.Column(db.String(255), nullable=True)
    season_number = db.Column(db.Integer, nullable=True)
    episode_number = db.Column(db.Integer, nullable=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    media_id = db.Column(db.Integer, db.ForeignKey('media.unique_id'), nullable=False)  # Added ForeignKey
    timestamp = db.Column(db.Integer, nullable=False) # I think were storing seconds?
    text = db.Column(db.String(500), nullable=False)

    season_number = db.Column(db.Integer, nullable=True)
    episode_number = db.Column(db.Integer, nullable=True)
    
class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    media_id = db.Column(db.Integer, db.ForeignKey('media.unique_id'), nullable=False)  # Added ForeignKey
    rating = db.Column(db.Float, nullable=False)

    season_number = db.Column(db.Integer, nullable=True)
    episode_number = db.Column(db.Integer, nullable=True)
