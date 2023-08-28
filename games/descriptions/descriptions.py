import json

from flask import Blueprint, render_template, request


descriptions_blueprint = Blueprint(
    'descriptions_bp', __name__)


@descriptions_blueprint.route('/gameDescription', methods=['GET'])
def descriptions():
    current_game = request.args.get('current_game')
    game_dict = request.args.get('game_dict')
    convert_to_dict = eval(game_dict)

    return render_template('gameDescription.html', current=convert_to_dict)
