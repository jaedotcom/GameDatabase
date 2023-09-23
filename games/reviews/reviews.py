from datetime import date

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange

import games.adapters.repository as repo
import games.reviews.services as services

from games.authentication.authentication import login_required
from games.forms.forms import CommentForm

# Configure Blueprint.
reviews_blueprint = Blueprint(
    'reviews_bp', __name__)


@reviews_blueprint.route('/write_reviews', methods=['GET', 'POST'])
@login_required
def write_game_review():
    # Obtain the user name of the currently logged in user.
    user_name = session['username']
    game_id = request.args.get('game_id', type=int)
    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with an game id, when subsequently called with a HTTP POST request, the review id remains in the
    # form.
    form = CommentForm()

    #     if form.validate_on_submit():
    #         # Get the game ID and review text from the form
    #
    #         review_text = form.comment.data
    #
    #         # Call a service function to post the review
    #         services.post_review(user_name, int(game_id), review_text, repo.repo_instance)
    #
    #         # Redirect to the game's details page or some other relevant page
    #         return redirect(url_for('games_bp.games_details', game_id=game_id))
    #
    #     # Render the review form template
    #     return render_template('browse/review_form.html', form=form)

    if form.validate_on_submit():
        # Successful POST, i.e. the comment text has passed data validation.
        # Extract the game id, representing the commented review, from the form.

        # game_id = int(form.game_id.data)
        game_id = request.form['game_id']
        review_text = form.comment.data
        # services.post_review(user_name, int(game_id), review_text, repo.repo_instance)
        # Use the service layer to store the new review.
        services.add_review(user_name, game_id, form.rating.data, review_text, repo.repo_instance)

        # Retrieve the review in dict form.
        review = services.get_reviews_for_game(game_id, repo.repo_instance)

        return redirect(url_for('descriptions_bp.gameDescription', game_id=game_id))

    # For a GET request or an unsuccessful POST, retrieve the game details and pass the form.
    game = repo.repo_instance.get_game_by_id(game_id)
    review = services.get_reviews_for_game(game_id, repo.repo_instance)

    # if request.method == 'GET':
    #     # Request is a HTTP GET to display the form.
    #     # Extract the game id, representing the review to comment, from a query parameter of the GET request.
    #     game_id = int(request.args.get('game'))
    #
    #     # Store the article id in the form.
    #     form.game_id.data = game_id
    # else:
    #     # Request is a HTTP POST where form validation has failed.
    #     # Extract the game id of the review being commented from the form.
    #     game_id = int(form.game_id.data)

    # For a GET or an unsuccessful POST, retrieve the review to comment in dict form, and return a Web page that allows
    # the user to enter a comment. The generated Web page includes a form object.


    return render_template(
        'browse/gameDescription.html',
        title='Game review',
        games=game,  # Pass the game data to the template
        reviews=review,  # Pass the reviews data to the template
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


# class CommentForm(FlaskForm):
#     comment = TextAreaField('Comment', [
#         DataRequired(),
#         Length(min=4, message='Your review is too short'),
#         ProfanityFree(message='Your review must not contain profanity')])
#     rating = TextAreaField('Rating', [
#         DataRequired(),
#         NumberRange(min=1, max=5, message='Rating must be between 1 and 5')
#     ])
#     game_id = HiddenField("game id")
#     submit = SubmitField('Submit')
