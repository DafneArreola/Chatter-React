from backend.database import db

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.Integer, nullable=False)
