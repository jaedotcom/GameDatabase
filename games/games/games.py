from flask import Blueprint, render_template, request, session, redirect, url_for
from games.authentication.authentication import login_required
from games.games import services
from games.home import services as sv
import games.adapters.repository as repo
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


games_bp = Blueprint('games_bp', __name__, url_prefix='/games')


class ReviewForm(FlaskForm):
    review_text = TextAreaField('Review', validators=[DataRequired()])
    submit = SubmitField('Submit Review')


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
    return render_template('browse/games.html', some_game=current_games, current_page=page, num_pages=total_pages,
                           all_genres=all_genres)


@games_bp.route('/game/<int:game_id>')
def game_description(game_id):
    user_name = session.get('username')
    game_details = services.get_games(game_id)
    form = ReviewForm()

    return render_template('browse/gameDescription.html', games=game_details, form=form, user_name=user_name)


