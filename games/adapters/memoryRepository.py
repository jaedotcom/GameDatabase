
import os.path

from typing import List


from games.adapters.repository import AbstractRepository

from games.domainmodel.model import Game, Genre, User, Publisher, Review, Wishlist
from games.adapters.datareader.csvdatareader import GameFileCSVReader

class MemoryRepository(AbstractRepository):
    # Articles ordered by date, not id. id is assumed unique.

    def __init__(self):
        self.__games = list()
        self.__genres = list()

    def add_game(self, game: Game):
        self.__games.append(game)

    def get_games(self) -> List[Game]:
        return self.__games

    def get_number_of_games(self):
        return len(self.__games)

    def get_genres(self) -> List[Genre]:
        return self.__genres

    def add_genre(self, genre: Genre):
        self.__genres.append(genre)


def populate(repo: AbstractRepository):

    dir_name = os.path.dirname(os.path.abspath(__file__))
    games_file_name = os.path.join(dir_name, "data/games.csv")
    reader = GameFileCSVReader(games_file_name)
    reader.read_csv_file()
    games = reader.dataset_of_games
    genres = reader.dataset_of_genres

    for game in games:
        repo.add_game(game)

    for genre in genres:
        repo.add_genre(genre)


