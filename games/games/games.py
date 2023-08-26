import os
import csv
from flask import Blueprint, render_template, request
import games.games.services
from games.games import services
import games.adapters.repository as repo

games_bp = Blueprint('games_bp', __name__)


@games_bp.route('/games')
def games():
    page = int(request.args.get('page', 1))
    games_per_page = 10

    all_games = services.get_games(repo.repo_instance)

    total_pages = (len(all_games) + games_per_page - 1) // games_per_page

    start_idx = (page - 1) * games_per_page
    end_idx = start_idx + games_per_page
    current_games = all_games[start_idx:end_idx]

    return render_template('games.html', some_game=current_games, current_page=page, num_pages=total_pages)


# def get_games_from_csv():
#     games = []
#     csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'adapters', 'data', 'games.csv')
#
#     with open(csv_path, newline='', encoding='utf-8') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             games.append(row)
#     return games
