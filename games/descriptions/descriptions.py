from flask import Blueprint, render_template, request
from games.home import services as sv
import games.adapters.repository as repo

descriptions_blueprint = Blueprint(
    'descriptions_bp', __name__)


@descriptions_blueprint.route('/gameDescription', methods=['GET'])
def descriptions():
    current_game = request.args.get('current_game')
    current_game_dict = eval(current_game)
    all_genres = sv.get_genres(repo.repo_instance)
    
    return render_template('gameDescription.html', current=current_game_dict, all_genres=all_genres)
