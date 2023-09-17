import os.path
from typing import List, Dict, Any
from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, Genre, User, Review
from games.adapters.datareader.csvdatareader import GameFileCSVReader


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.__reviews = list()
        self.__games = list()
        self.__genres = list()
        self.__games_by_genre = dict()
        self.__users = list()

    def add_user(self, user: User):
        for already_user in self.__users:
            if already_user.username == user.username:
                return "Username already taken."
        self.__users.append(user)

    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.username == user_name), None)

    def add_game(self, game: Game):
        self.__games.append(game)
        for genre_name in game.genres:
            if genre_name not in self.__games_by_genre:
                self.__games_by_genre[genre_name] = []
            self.__games_by_genre[genre_name].append(game)

    def get_games(self) -> List[Game]:
        return self.__games

    def get_game_by_id(self, game_id) -> Any | None:
        for game in self.__games:
            if game.game_id == game_id:
                return game
        return None

    def get_number_of_games(self):
        return len(self.__games)

    def get_genres(self) -> List[Genre]:
        return self.__genres

    def add_genre(self, genre: Genre):
        self.__genres.append(genre)

    def get_games_by_genre(self, genre_name: str) -> List[Game]:
        return self.__games_by_genre.get(genre_name, [])

    def add_review(self, review: Review) -> Review:
        self.__reviews.append(review)
        return review

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
