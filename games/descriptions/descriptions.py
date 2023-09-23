from flask import Blueprint, render_template, request, session
from games.home import services as sv
from games.games import services as game_services
from games.profile import services as profile_services
import games.adapters.repository as repo
from games.authentication.authentication import login_required


descriptions_blueprint = Blueprint(
    'descriptions_bp', __name__)


@descriptions_blueprint.route('/gameDescription', methods=['GET'])
def descriptions():
    global current_game_dict
    current_game = request.args.get('current_game')
    game_id = request.args.get('current_game_id')
    try:
        current_game_dict = eval(current_game)
    except SyntaxError:
        all_games = game_services.get_games(repo.repo_instance)
        for game in all_games:
            if game.get('game_id') == int(game_id):
                current_game_dict = game
    all_genres = sv.get_genres(repo.repo_instance)
    return render_template('browse/gameDescription.html', games=current_game_dict, all_genres=all_genres)


@descriptions_blueprint.route('/gameDescription/<int:game_id>', methods=['GET'])
def search_game_description(game_id):
    all_games = game_services.get_games(repo.repo_instance)
    current_game_dict = None

    for game in all_games:
        if game.get('game_id') == game_id:
            current_game_dict = game
            break

    if current_game_dict is None:
        pass

    all_genres = sv.get_genres(repo.repo_instance)
    return render_template('browse/gameDescription.html', games=current_game_dict, all_genres=all_genres)


@descriptions_blueprint.route('/gameDescription/favourite', methods=['GET', 'POST'])
@login_required
def favourite():
    current_game = request.args.get('current_game')
    game_id = request.args.get('current_game_id')

    try:
        current_game_dict = eval(current_game)
    except SyntaxError:
        all_games = game_services.get_games(repo.repo_instance)
        for game in all_games:
            if game.get('game_id') == int(game_id):
                current_game_dict = game

    user = session.get('username')
    if user:
        current_user = profile_services.get_user(user, repo.repo_instance)

        if current_user:
            game1 = repo.repo_instance.get_game_by_id(current_game_dict['game_id'])

            if game1:
                profile_services.add_to_favourites(current_user, game1)

    all_genres = sv.get_genres(repo.repo_instance)
    return render_template('browse/gameDescription.html', games=current_game_dict, all_genres=all_genres)

