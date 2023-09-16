from flask import Blueprint, render_template, request
from games.games.services import get_games
from games.home import services
import games.adapters.repository as repo

profile_blueprint = Blueprint('profile_bp', __name__)


@profile_blueprint.route('/profile')
def profile():
    return render_template('profile.html')