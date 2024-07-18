from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class CommentForm(FlaskForm):
    comment = StringField('comment', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    user_id = StringField('user_id', validators=[DataRequired()])
    timestamp = StringField('timestamp', validators=[DataRequired()]) 

    submit = SubmitField('submit')