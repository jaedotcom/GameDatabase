from games.adapters.repository import AbstractRepository
from functools import cmp_to_key



def get_game_by_id(game_id, repo: AbstractRepository):
    for game in repo:
        if game.game_id == game_id:
            return game
    return None


def get_number_of_games(repo: AbstractRepository):
    return repo.get_number_of_games()


def get_games(repo: AbstractRepository):
    games = repo.get_games()
    sorted_games = sorted(games, key=cmp_to_key(compare_games_by_title))
    game_dicts = []
    for game in sorted_games:
        game_genres = game.genres
        genre_names = []
        for i in game_genres:
            genre_names.append(i.genre_name)
        game_dict = {
            'game_id': game.game_id,
            'title': game.title,
            'game_release_date': game.release_date,
            'price': game.price,
            'description': game.description,
            'image_url': game.image_url,
            'genres': genre_names
        }
        game_dicts.append(game_dict)
    return game_dicts


def compare_games_by_title(game1, game2):
    return (game1.title > game2.title) - (game1.title < game2.title)


def compare_games_by_release_date(game1, game2):
    return (game1.release_date > game2.release_date) - (game1.release_date < game2.release_date)


def get_games_by_search_key(search_key: str, repo):
    games = repo.get_games()
    if not search_key or not isinstance(search_key, str):
        raise ValueError("Invalid search key")
    matching_games = []
    for game in games:
        if search_key.lower() in game.title.lower():
            matching_games.append(game)
    return matching_games

