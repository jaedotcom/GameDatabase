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

    all_genres = []
    game_titles = []

    for game in all_games:
        for g in game['genres']:
            if g not in all_genres:
                all_genres.append(g.lower())

    for game in all_games:
        if game['title'] not in game_titles:
            game_titles.append(game['title'].lower())

    found_games = []

    for game in all_games:
        if (search.lower() in game_titles) and (genre_filter.lower() in all_genres):
            found_games.append(game)
    print("Search is " + search.lower())
    print("Genre_filter is " + genre_filter.lower())
    print(found_games)
    print(all_genres)
    print(game_titles)
    return render_template('gameDescription.html', search_query=search, games=found_games, all_genres=all_genres)