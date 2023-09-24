from datetime import date

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange

import games.adapters.repository as repo
import games.reviews.services as services

from games.authentication.authentication import login_required



# Configure Blueprint.
reviews_blueprint = Blueprint(
    'reviews_bp', __name__)


@reviews_blueprint.route('/write_game_reviews', methods=['GET', 'POST'])
@login_required
def write_game_review():

    form = CommentForm()
    user_name = session.get('username')

    #CRASHES here : ...
    if form.validate_on_submit():
        game_id = form.game_id.data

        if game_id:
            game_id = int(game_id)
            review_text = str(form.comment.data)
            rating = int(form.rating.data)

            services.add_review(game_id, review_text, user_name, rating, repo.repo_instance)

            # Retrieve the review in dict form.
            # review = services.get_reviews_for_game(game_id, repo.repo_instance)

            return redirect(url_for('descriptions_bp.descriptions_with_reviews', game_id=game_id))
            #return redirect(url_for('descriptions_bp.search_game_description', game_id=game_id))
            #return redirect(url_for('descriptions_bp.game_description'))

    game_id = request.args.get('game_id', type=int)
    game = repo.repo_instance.get_game_by_id(game_id)
    #review = services.get_reviews_for_game(int(game_id), repo.repo_instance)
    review = []
    if game_id is not None:
        review = services.get_reviews_for_game(game_id, repo.repo_instance)

    return render_template(
        'browse/gameDescription.html',
        title='Game review',
        games=game,
        reviews=review,
        form=form,
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class CommentForm(FlaskForm):
    comment = StringField('Comment', [
        DataRequired(),
        Length(min=4, message='Your review is too short'),
        ProfanityFree(message='Your review must not contain profanity')])

    rating = IntegerField('Rating', [
        DataRequired(),
        NumberRange(min=1, max=5, message='Rating must be between 1 and 5')
    ])
    game_id = HiddenField("game id")
    submit = SubmitField(label="Submit")
