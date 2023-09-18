from flask import Blueprint, render_template, request
from games.games.services import get_games
from games.home import services
import games.adapters.repository as repo
from games.profile import services as profile_services
from games.domainmodel.model import User

profile_blueprint = Blueprint('profile_bp', __name__)


@profile_blueprint.route('/profile')
def profile():
    user = request.args.get('current_user')
    print(user)
    #favourite_list = profile_services.get_favourites(user)
    return render_template('profile.html')