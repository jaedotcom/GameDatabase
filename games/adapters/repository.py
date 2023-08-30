import abc
from typing import List
from games.domainmodel.model import Game, Genre

repo_instance = None


class RepositoryException(Exception):
    def __init__(self, message=None):
        print(f'RepositoryException: {message}')


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add_game(self, game: Game):
        """Add a game to repository list of aames"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_games(self) -> List[Game]:
        """Returns list of games"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_games(self):
        """Returns no. of games in repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self) -> List[Genre]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        raise NotImplementedError

    @abc.abstractmethod
    def get_games_by_genre(self, genre_name: str) -> List[Game]:
        raise NotImplementedError



