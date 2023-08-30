
from flask import Blueprint, render_template, request
from games.games import services
from games.home import services as sv
import games.adapters.repository as repo

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
    return render_template('games.html', some_game=current_games, current_page=page, num_pages=total_pages, all_genres=all_genres)



