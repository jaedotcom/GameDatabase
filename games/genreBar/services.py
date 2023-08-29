from games.adapters.repository import AbstractRepository
from functools import cmp_to_key

def get_genres(repo: AbstractRepository):
    genres = repo.get_genres()
    game_genres = []
    for genre in genres:
        game_genres.append(genre.genre_name)
    return game_genres

def get_number_of_games(repo: AbstractRepository):
    return repo.get_number_of_games()


def get_games_by_genre(repo: AbstractRepository, genre_name):
    games = repo.get_games_by_genre(genre_name)
    sorted_games = sorted(games, key=cmp_to_key(compare_games_by_title))
    game_dicts = []
    for game in sorted_games:
        game_dict = {
            'title': game.title,
            'release_year': game.release_date
        }
        game_dicts.append(game_dict)
    return game_dicts

def compare_games_by_title(game1, game2):
    return (game1.title > game2.title) - (game1.title < game2.title)

def compare_games_by_release_date(game1, game2):
    return (game1.release_date > game2.release_date) - (game1.release_date < game2.release_date)

#def get_games_sorted_by_release_date(repo: AbstractRepository):
 #   games = repo.get_games()
  #  sorted_games = sorted(games, key=cmp_to_key(compare_games_by_release_date))

   # game_dicts = []
    #for game in sorted_games:
     #   game_dict = {
      #      'game_id': game.game_id,
       #     'title': game.title,
        #    'game_release_date': game.release_date,
        #}
        #game_dicts.append(game_dict)
    #return game_dicts

