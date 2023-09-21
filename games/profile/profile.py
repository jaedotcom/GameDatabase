from flask import Blueprint, render_template, request, session
from games.games.services import get_games
from games.home import services
import games.adapters.repository as repo
from games.profile import services as profile_services
from games.domainmodel.model import User

profile_blueprint = Blueprint('profile_bp', __name__)


@profile_blueprint.route('/profile', methods=['GET', 'POST'])
def profile():
    #get current user from session???
    user = session['username']
    # current_game = request.args.get('current_game')
    # print(current_game)
    # #get user from user list in memory repo
    current_user = profile_services.get_user(user, repo.repo_instance)
    favourite_list = profile_services.get_favourites(current_user)
    # need to add favourite list to profile.html and pass favourite_list when render template.
    return render_template('profile.html', favourites=favourite_list)


