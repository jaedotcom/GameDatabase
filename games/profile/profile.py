from flask import Blueprint, render_template, request, session, redirect, url_for
from games.games.services import get_games
from games.home import services
import games.adapters.repository as repo
from games.profile import services as profile_services
from games.games import services as game_services
from games.domainmodel.model import User
from games.authentication.authentication import login_required

profile_blueprint = Blueprint('profile_bp', __name__)


@profile_blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = session['username']
    current_user = profile_services.get_user(user, repo.repo_instance)
    if current_user is None:
        return redirect(url_for("authentication_bp.login"))

    favourite_list = current_user.favourite_games
    print(current_user.username)
    print(favourite_list)
    return render_template('profile.html', favourites=favourite_list, current_user=current_user)


@profile_blueprint.route('/profile/delete/<int:game_id>', methods=['GET', 'POST'])
@login_required
def delete_favourite(game_id):
    # Get user
    user = session['username']
    current_user = profile_services.get_user(user, repo.repo_instance)

    game1 = repo.repo_instance.get_game_by_id(game_id)

    profile_services.remove_from_fav(game1, current_user, repo.repo_instance)

    return redirect(url_for('profile_bp.profile'))
