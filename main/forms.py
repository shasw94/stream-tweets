from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class HastagSearchForm(FlaskForm):
    hashtag = StringField('Hashtag', validators=[DataRequired()])
    submit = SubmitField('HashTag Search')

class UserIdSearchForm(FlaskForm):
    user_id = StringField('User Id', validators=[DataRequired()])
    submit = SubmitField('User Id Search')
