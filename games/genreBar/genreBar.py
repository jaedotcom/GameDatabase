from flask import Blueprint, render_template
from games.home import services
import games.adapters.repository as repo


genreBar_blueprint = Blueprint(
    'genreBar_bp', __name__)


@genreBar_blueprint.route('/genreBar', methods=['GET'])
def genreBar():
    all_genres = services.get_genres(repo.repo_instance)
    return render_template('genreBar.html', all_genres=all_genres)