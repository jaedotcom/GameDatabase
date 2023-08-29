from flask import Blueprint, render_template, request

from games.games.services import get_games
from games.home import services
import games.adapters.repository as repo


home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET', 'POST'])
def home():
    all_genres = services.get_genres(repo.repo_instance)
    print('form submitted to here')
    return render_template('home.html', all_genres=all_genres)


@home_blueprint.route('/search', methods=('GET', 'POST'))
def search_results():
    if request.method == 'POST':
        search = request.form['search']
    else:
        search = 'failure'

    print(search)
    all_games = get_games(repo.repo_instance)
    found_games = []

    for game in all_games:
        if search.lower() in game['title'].lower():
            found_games.append(game)

    return render_template('gameDescription.html', current=found_games, search_query=search, games=found_games)