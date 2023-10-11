from games.adapters.repository import AbstractRepository
from games.games import services as game_services


def get_games_by_genre(repo: AbstractRepository, genre_name, search_query=None):
    games = game_services.get_games(repo)
    genre_hit = []
    for game in games:
        game_genres = game.get('genres')
        for i in game_genres:
            if i == genre_name:
                genre_hit.append(game.get('game_id'))
    if search_query:
        search_query = search_query.replace('%', '')
        filtered_games = [game for game in genre_hit if search_query.lower() in game['title'].lower()]
    else:
        filtered_games = genre_hit
    return filtered_games


