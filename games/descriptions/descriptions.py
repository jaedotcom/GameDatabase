from flask import Blueprint, render_template


descriptions_blueprint = Blueprint(
    'descriptions_bp', __name__)


@descriptions_blueprint.route('/gameDescription', methods=['GET'])
def descriptions():
    return render_template('gameDescription.html')
