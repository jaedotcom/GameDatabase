import pytest
import os.path
from typing import List
from games.adapters.datareader.csvdatareader import GameFileCSVReader
from games.domainmodel.model import Game, Genre
from games.adapters.memoryRepository import MemoryRepository
from games.adapters.repository import AbstractRepository

class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__games = list()
        self.__genres = list()
        self.__games_by_genre = dict()

    def add_game(self, game: Game):
        self.__games.append(game)
        for genre_name in game.genres:
            if genre_name not in self.__games_by_genre:
                self.__games_by_genre[genre_name] = []
            self.__games_by_genre[genre_name].append(game)

    def get_games(self) -> List[Game]:
        return self.__games

    def get_number_of_games(self):
        return len(self.__games)

    def get_genres(self) -> List[Genre]:
        return self.__genres

    def add_genre(self, genre: Genre):
        self.__genres.append(genre)

    def get_games_by_genre(self, genre_name: str) -> List[Game]:
        return self.__games_by_genre.get(genre_name, [])


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


class TestRepository:

    @pytest.fixture
    def repo(self):
        return MemoryRepository()



class TestRepository:


    @pytest.fixture
    def repo(self):
        return MemoryRepository()

    def test_add_game_object(self, repo):
        new_game = Game(12347, 'I hate writing testings 3')
        repo.add_game(new_game)
        retrieved_game = repo.get_games()
        assert retrieved_game is not None
        assert retrieved_game[0].game_id == 12347
        assert retrieved_game[0].title == 'I hate writing testings 3'


    def test_retrieve_game_object(self, repo):
        new_game = Game(12349, 'I hate writing testings 4')
        new_game.add_genre(Genre('Action'))
        repo.add_game(new_game)
        retrieved_game = repo.get_games_by_genre("Action")
        assert retrieved_game is not None
        assert len(retrieved_game) == 0

    def test_retrieve_correct_number_of_game_objects(self, repo):
        sample_game_data = [Game(123410, 'I hate writing testings 6'), Game(12346, 'I hate writing testings 2')]
        repo.add_game(Game(123410, 'I hate writing testings 6'))
        repo.add_game(Game(12346, 'I hate writing testings 2'))
        num_games = repo.get_number_of_games()
        assert num_games == len(sample_game_data)

    def test_number_of_unique_genres(self, repo):
        sample_game_data1 = Game(123411, 'I hate writing testings 8')
        sample_game_data2 = Game(123499, 'I hate writing testings 12')
        sample_game_data1.add_genre(Genre('Horror'))
        sample_game_data1.add_genre(Genre('R18'))
        sample_game_data1.add_genre(Genre('Love Story'))
        sample_game_data2.add_genre(Genre('Adventure'))
        sample_game_data2.add_genre(Genre('R18'))
        repo.add_game(Game(123411, 'I hate writing testings 8'))
        repo.add_game(Game(123499, 'I hate writing testings 12'))
        all_game_number = repo.get_number_of_games()
        assert all_game_number == 2
        all_game = repo.get_games()
        unique_genres = set()
        for game in all_game:
            for i in game.genres:
                unique_genres.add(i)
        assert type(unique_genres) is set
        list(set(unique_genres))
        assert len(unique_genres) == 0
        sample_game_data1.add_genre(Genre('Adventure'))
        sample_game_data2.add_genre(Genre('Love Story'))
        assert len(unique_genres) == 0
        assert len(unique_genres) == 0

    def test_add_new_genre(self, repo):
        new_genre = Genre("Racing")
        initial_num_genres = len(repo.get_genres())
        repo.add_genre(new_genre)
        updated_num_genres = len(repo.get_genres())
        assert updated_num_genres == initial_num_genres + 1


    def test_get_games_by_genre_name(self, repo):
        sample_game_data1 = Game(123411, 'I hate writing testings 8')
        sample_game_data1.add_genre(Genre('Adventure'))
        repo.add_game(Game(123411, 'I hate writing testings 8'))
        all_game = repo.get_games()
        for game in all_game:
            game.add_genre(Genre('Adventure'))
        games_by_genre = repo.get_games_by_genre("Action")
        assert len(games_by_genre) == 0
        games_by_genre1 = repo.get_games_by_genre("Funny")
        assert len(games_by_genre1) == 0







