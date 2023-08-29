from games.adapters.repository import AbstractRepository
from functools import cmp_to_key
from games.home import services as home_services
from games.games import services as game_services

def get_genres(repo: AbstractRepository):
    genres = repo.get_genres()
    game_genres = []
    for genre in genres:
        game_genres.append(genre.genre_name)
    return game_genres

def get_number_of_games(repo: AbstractRepository):
    return repo.get_number_of_games()

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

def get_genre_lists():
    genre_list = home_services.get_genres()

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

