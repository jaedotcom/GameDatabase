from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Review, Game, User


def get_game(repo: AbstractRepository, game_id: int):
    games = repo.get_games()
    for game in games:
        if game.game_id == game_id:
            return game


def add_review_to_database(repo: AbstractRepository, review: Review):
    repo.add_review(review)


def add_to_faves(current_game: Game, current_user: User, repo: AbstractRepository):
    current_user.add_favourite_game(current_game)
    repo.add_user(current_user)