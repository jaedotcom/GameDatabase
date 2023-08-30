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
    global genre_filter
    if request.method == 'POST':
        search = request.form['search'].strip()
        genre_filter = request.form['genre']
    else:
        search = 'failure'

    print(search)
    all_games = get_games(repo.repo_instance)
    print(all_games)
    all_genres = set()
    game_titles = set()

    for game in all_games:
        for g in game['genres']:
            all_genres.update(g.lower())

    for game in all_games:
        game_titles.update(game['title'].lower())

    found_games = []

    for game in all_games:
        if (not search or search.lower() in game_titles) and \
                (not genre_filter or genre_filter.lower() in game['genres']):
            found_games.append(game)
            print(found_games)

    return render_template('gameDescription.html', search_query=search, games=found_games, all_genres=all_genres)