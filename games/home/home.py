from flask import Blueprint, render_template, request

from games.games.services import get_games
from games.home import services
import games.adapters.repository as repo


home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET', 'POST'])
def home():
    all_genres = services.get_genres(repo.repo_instance)
    return render_template('home.html', all_genres=all_genres)


@home_blueprint.route('/search', methods=('GET', 'POST'))
def search_results():
    global genre_filter
    if request.method == 'POST':
        search = request.form['search'].strip()
        genre_filter = request.form['genre'].strip()
    else:
        search = 'failure'

    all_games = get_games(repo.repo_instance)
    game_titles = []
    all_genres = set()

    for game in all_games:
        for g in game['genres']:
            all_genres.add(g.lower())

    all_genres = list(set(all_genres))

    for game in all_games:
        if game['title'] not in game_titles:
            game_titles.append(game['title'].lower())

    found_games = []

    for game in all_games:
        list_of_genres = game['genres']
        if (search.lower() in game_titles) and (genre_filter.lower() in all_genres):
            if game['title'].lower() == search.lower():
                if genre_filter in list_of_genres:
                    found_games.append(game)

    return render_template('gameSearbarResult.html', search_query=search, games=found_games, all_genres=all_genres)