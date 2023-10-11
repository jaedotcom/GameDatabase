from games.domainmodel.model import User, Game
from games.adapters.repository import AbstractRepository


def get_favourites(user: User):
    return user.favourite_games


def add_to_favourites(user: User, game: Game):
    user.add_favourite_game(game)


def get_user(username: str, repo: AbstractRepository):
    user = repo.get_user(username)
    return user


def delete_favourites(user: User, game: Game):
    user.remove_favourite_game(game)

def remove_from_fav(current_game: Game, current_user: User, repo: AbstractRepository):
    current_user.remove_favourite_game(current_game)
    repo.update_user(current_user)

