from games.adapters.repository import AbstractRepository


def get_game(repo: AbstractRepository, game_id: int ):
    games = repo.get_games()
    for game in games:
        if game.game_id == game_id:
            return game