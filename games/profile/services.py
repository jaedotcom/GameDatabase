from games.domainmodel.model import Wishlist, User, Game
from games.adapters.repository import AbstractRepository


def get_favourites(user: User):
    return user.favourite_games


def add_to_favourites(user: User, game: Game):
    user.add_favourite_game(game)


def get_user(username: str, repo: AbstractRepository):
    user = repo.get_user(username)
    return user



