from flask import Blueprint, render_template

games_blueprint = Blueprint(
    'games_bp', __name__)


@games_blueprint.route('/gameDescription', methods=['GET'])
def home():
    return render_template(
        'games.html',

    )
