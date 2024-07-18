from app import db

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    user_id = db.Column(db.String(100))
    comment = db.Column(db.String(1000))
    timestamp = db.Column(db.String(100))
