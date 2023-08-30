from flask import Blueprint, render_template, request
from games.games import services
import games.adapters.repository as repo


search_bp = Blueprint('search_bp', __name__)


@search_bp.route('/search/<search>', methods=('GET', 'POST'))
def search_results(search):
    print(search)
    if request.method == 'POST':
        search = request.form['search']

    print(search)

    all_games = services.get_games(repo.repo_instance)
    for game in all_games:
        if game.get('game_id') == game(search).id:
            current_games = game
    return render_template('gameDescription.html',some_game=current_games)


