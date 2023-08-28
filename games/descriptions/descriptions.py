from flask import Blueprint, render_template, request


descriptions_blueprint = Blueprint(
    'descriptions_bp', __name__)


@descriptions_blueprint.route('/gameDescription', methods=['GET'])
def descriptions():
    current_game = request.args.get('current_game')
    current_game_dict = eval(current_game)
    print(current_game_dict['price'])


    return render_template('gameDescription.html', current=current_game_dict)
