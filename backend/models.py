from backend.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)



class Comment(db.Model):
   #__tablename__ = 'Comments'
   id = db.Column(db.Integer, primary_key=True)
   text = db.Column(db.String(1000))
   timestamp = db.Column(db.String(8))
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Rating(db.Model):
   #__tablename__ = 'Ratings'
   id = db.Column(db.Integer, primary_key=True)
   rating = db.Column(db.Integer)
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
