
from flask import Blueprint, render_template


search_bp = Blueprint('search_bp', __name__)


@search_bp.route('/games')
def search_results():
    return render_template('games.html')


