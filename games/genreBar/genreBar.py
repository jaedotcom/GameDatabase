from flask import Blueprint, render_template, request
from games.home import services
from .services import get_games_by_genre
from games.games import services as game_services
import games.adapters.repository as repo

genreBar_blueprint = Blueprint('genreBar_bp', __name__)


def paginate_games(games, page, games_per_page):
    start_idx = (page - 1) * games_per_page
    end_idx = start_idx + games_per_page
    paginated_games = games[start_idx:end_idx]
    return paginated_games


@genreBar_blueprint.route('/genreBar/<genre>', methods=['GET'])
def genre_bar(genre: str):
    all_genres = services.get_genres(repo.repo_instance)
    selected_genre = genre
    genre_games = get_games_by_genre(repo.repo_instance, selected_genre)
    all_games = game_services.get_games(repo.repo_instance)
    refined_games = []
    for id in genre_games:
        for game in all_games:
            if game.get('game_id') == id:
                refined_games.append(game)


    games_per_page = 10  # You can adjust this value as needed
    page = int(request.args.get('page', 1))
    paginated_games = paginate_games(refined_games, page, games_per_page)

    num_pages = (len(refined_games) + games_per_page - 1) // games_per_page

    return render_template(
        'gameGenre.html',
        games=paginated_games,
        all_genres=all_genres,
        selected_genre=selected_genre,
        current_page=page,
        num_pages=num_pages,
    )
