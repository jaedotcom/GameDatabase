from flask import Blueprint, render_template, request
from games.games.services import get_games
from games.home import services
import games.adapters.repository as repo


home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET', 'POST'])
def home():
    all_genres = services.get_genres(repo.repo_instance)
    return render_template('home/home.html', all_genres=all_genres)

@home_blueprint.route('/search_genres', methods=('GET', 'POST'))
def search_genres():
    if request.method == 'POST':
        search = request.form['search'].strip()
    else:
        search = 'failure'
    all_games = get_games(repo.repo_instance)
    found_games = []
    for game in all_games:
        for genre in game['genres']:
            if search.lower() in genre.lower():
                found_games.append(game)

    print(found_games)
    return render_template('search/gameSearchBarResult.html', search_query=search, games=found_games)

@home_blueprint.route('/search_publishers', methods=('GET', 'POST'))
def search_publishers():
    if request.method == 'POST':
        search = request.form['search'].strip()
    else:
        search = 'failure'
    all_games = get_games(repo.repo_instance)
    found_games = []
    for game in all_games:
        if search.lower() in game['publisher'].publisher_name.lower():
            found_games.append(game)
    print(found_games)
    return render_template('search/gameSearchBarResult.html', search_query=search, games=found_games)


@home_blueprint.route('/search_titles', methods=('GET', 'POST'))
def search_titles():
    if request.method == 'POST':
        search = request.form['search'].strip()
    else:
        search = 'failure'
    all_games = get_games(repo.repo_instance)
    found_games = []
    for game in all_games:
        if search.lower() in game['title'].lower():
            found_games.append(game)
    print(found_games)
    return render_template('search/gameSearchBarResult.html', search_query=search, games=found_games)


