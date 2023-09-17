from flask import Blueprint, render_template, request, session, redirect, url_for
from games.authentication.authentication import login_required
from games.games import services
from games.home import services as sv
import games.adapters.repository as repo
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

games_bp = Blueprint('games_bp', __name__)


@games_bp.route('/games')
def games():
    page = int(request.args.get('page', 1))
    games_per_page = 22
    all_games = services.get_games(repo.repo_instance)
    total_pages = (len(all_games) + games_per_page - 1) // games_per_page
    start_idx = (page - 1) * games_per_page
    end_idx = start_idx + games_per_page
    current_games = all_games[start_idx:end_idx]
    all_genres = sv.get_genres(repo.repo_instance)
    return render_template('games.html', some_game=current_games, current_page=page, num_pages=total_pages,
                           all_genres=all_genres)


@games_bp.route('/review', methods=['GET', 'POST'])
@login_required
def post_a_review():
    # Obtain the user name of the currently logged in user.
    user_name = session['username']

    class ReviewForm(FlaskForm):
        review_text = TextAreaField('Review', validators=[DataRequired()])
        submit = SubmitField('Submit Review')

    form = ReviewForm()

    if form.validate_on_submit():
        # Get the game ID and review text from the form
        game_id = request.form['game_id']
        review_text = form.review_text.data

        # Call a service function to post the review
        services.post_review(user_name, int(game_id), review_text, repo.repo_instance)

        # Redirect to the game's details page or some other relevant page
        return redirect(url_for('games_bp.games_details', game_id=game_id))

    # Render the review form template
    return render_template('review_form.html', form=form)


@games_bp.route('/rate', methods=['GET', 'POST'])
@login_required
def post_a_rating():
    # Obtain the user name of the currently logged in user.
    user_name = session['username']

    if request.method == 'POST':
        # Get the game ID and rating from the form
        game_id = request.form['game_id']
        rating = request.form['rating']

        # Call a service function to post the rating
        services.post_rating(user_name, game_id, rating, repo.repo_instance)

        # Redirect to the game's details page or some other relevant page
        return redirect(url_for('games_bp.games_details', game_id=game_id))

    # Render the rating form template
    return render_template('rating_form.html')  # Create a rating form template as needed
