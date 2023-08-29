from flask import Blueprint, render_template, request
from games.home import services
from .services import get_games_by_genre
from games.games import services as game_services
import games.adapters.repository as repo
from .. import MemoryRepository


genreBar_blueprint = Blueprint(
    'genreBar_bp', __name__)


@genreBar_blueprint.route('/genreBar', methods=['GET'])
def genreBar():
    all_genres = services.get_genres(repo.repo_instance)
    selected_genre = request.args.get('genre')
    print(selected_genre)
    if selected_genre:
        genre_games = get_games_by_genre(repo.repo_instance, selected_genre)
    else:
        genre_games = []

    all_games = game_services.get_games(repo.repo_instance)
    refined_games = []
    for id in genre_games:
        for game in all_games:
            if game.get('game_id') == id:
                refined_games.append(game)
    return render_template('genreBar.html', all_genres=refined_games, genre_games=genre_games)


@genreBar_blueprint.route('/genreBar/<genre>', methods=['GET'])
def genre_bar(genre: str):
    all_genres = services.get_genres(repo.repo_instance)
    #selected_genre = request.args.get('genre')
    selected_genre = genre
    print(selected_genre)

    genre_games = get_games_by_genre(repo.repo_instance, selected_genre)
    print(genre_games)

    all_games = game_services.get_games(repo.repo_instance)
    refined_games = []
    for id in genre_games:
        print(id)
        for game in all_games:
            if game.get('game_id') == id:
                refined_games.append(game)

    print(refined_games)

    return render_template('gameGenre.html', games=refined_games, all_genres=all_genres)
