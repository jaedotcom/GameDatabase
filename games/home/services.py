from games.adapters.repository import AbstractRepository


def get_genres(repo: AbstractRepository):
    genres = repo.get_genres()
    game_genres = []
    for genre in genres:
        game_genres.append(genre.genre_name)
    return game_genres
