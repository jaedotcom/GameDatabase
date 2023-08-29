from flask import Blueprint, render_template, request
from games.home import services as sv
from games.games import services as game_services
import games.adapters.repository as repo

descriptions_blueprint = Blueprint(
    'descriptions_bp', __name__)


@descriptions_blueprint.route('/gameDescription', methods=['GET'])
def descriptions():
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

    return render_template('gameDescription.html', current=current_game_dict, all_genres=all_genres)
