from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class HastagSearchForm(FlaskForm):
    '''
    Creates form field for accepting hashtags
    '''
    hashtag = StringField('Hashtag', validators=[DataRequired()])
    submit = SubmitField('HashTag Search')

class UserIdSearchForm(FlaskForm):
    '''
    Creates form field for accepting username of twitter
    '''
    user_id = StringField('User Id', validators=[DataRequired()])
    submit = SubmitField('User Id Search')
