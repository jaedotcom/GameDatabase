from flask import Blueprint, render_template, request


descriptions_blueprint = Blueprint(
    'descriptions_bp', __name__)


@descriptions_blueprint.route('/gameDescription', methods=['GET'])
def descriptions():
    current_title = request.args.get('title')
    return render_template('gameDescription.html', current=current_title)
