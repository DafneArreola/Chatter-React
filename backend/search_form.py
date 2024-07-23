from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired 


class SearchForm(FlaskForm):
    name_search = StringField('name_search', validators=[DataRequired()])
    submit = SubmitField('submit')