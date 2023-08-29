from flask import Blueprint, render_template, request
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
    return render_template('home.html')