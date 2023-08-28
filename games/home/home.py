from flask import Blueprint, render_template
from games.home import services
import games.adapters.repository as repo


home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    all_genres = services.get_genres(repo.repo_instance)
    return render_template('home.html', all_genres=all_genres)
