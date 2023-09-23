from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange


class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', [
        DataRequired(),
        Length(min=4, message='Your review is too short')])
    rating = HiddenField('Rating', [
        DataRequired(),
        NumberRange(min=1, max=5, message='Rating must be between 1 and 5')])
    game_id = HiddenField("game id")
    submit = SubmitField('Submit')