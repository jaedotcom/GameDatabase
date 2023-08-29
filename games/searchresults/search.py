
from flask import Blueprint, render_template, request


search_bp = Blueprint('search_bp', __name__)


@search_bp.route('/search/<search>', methods=('GET', 'POST'))
def search_results(search):
    print(search)
    if request.method == 'POST':
        search = request.form['search']

    print(search)
    return render_template('home.html')


