from flask import Blueprint, render_template, request
from games.home import services
from .services import get_games_by_genre
import games.adapters.repository as repo


genreBar_blueprint = Blueprint(
    'genreBar_bp', __name__)


@genreBar_blueprint.route('/genreBar', methods=['GET'])
def genreBar():
    all_genres = services.get_genres(repo.repo_instance)

    selected_genre = request.args.get('genre')
    if selected_genre:
        genre_games = get_games_by_genre(repo.repo_instance, selected_genre)
    else:
        genre_games = []

    return render_template('genreBar.html', all_genres=all_genres, genre_games=genre_games)