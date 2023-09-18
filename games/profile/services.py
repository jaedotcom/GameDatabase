from games.domainmodel.model import Wishlist, User, Game


def get_favourites(user: User):
    return user.favourite_games


def add_to_favourites(user: User, game: Game):
    user.add_favourite_game(game)

