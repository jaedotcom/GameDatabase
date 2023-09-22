from flask import Blueprint, render_template, request, session
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
    favourite_list = profile_services.get_favourites(current_user)
    for fave in favourite_list:
        print(type(fave))
        print(fave.game_id)
    return render_template('profile.html', favourites=favourite_list)


@profile_blueprint.route('/profile/delete', methods=['GET', 'POST'])
@login_required
def delete_favourite():
    #gets game
    current_game = request.args.get('current_game')
    game_id = request.args.get('current_id')

    try:
        current_game_dict = eval(current_game)
    except SyntaxError:
        all_games = game_services.get_games(repo.repo_instance)
        for game in all_games:
            if game.get('game_id') == int(game_id):
                current_game_dict = game

    #gets user
    user = session['username']
    current_user = profile_services.get_user(user, repo.repo_instance)

    game1 = repo.repo_instance.get_game_by_id(current_game_dict['game_id'])

    #delete game from users favourite list
    profile_services.delete_favourites(current_user, game1)
    favourite_list = profile_services.get_favourites(current_user)
    return render_template('profile.html', favourites=favourite_list)


