import csv
import os.path
from pathlib import Path
from datetime import date, datetime
from typing import List
import games.adapters.repository as repo

from games.adapters.repository import AbstractRepository

from games.domainmodel.model import Game, Genre, User, Publisher, Review, Wishlist
from games.adapters.datareader.csvdatareader import GameFileCSVReader

class MemoryRepository(AbstractRepository):
    # Articles ordered by date, not id. id is assumed unique.

    def __init__(self):
        self.__games = list()
        # self.__games_index = dict()
        # self.__tags = list()
        # self.__users = list()
        # self.__reviews = list()

    def add_game(self, game: Game):
        self.__games.append(game)

    def get_games(self) -> List[Game]:
        return self.__games

    def get_number_of_games(self):
        return len(self.__games)

#
# def read_csv_file(filename: str):
#     with open(filename, encoding='utf-8-sig') as infile:
#         reader = csv.reader(infile)
#
#         # Read first line of the the CSV file.
#         headers = next(reader)
#
#         # Read remaining rows from the CSV file.
#         for row in reader:
#             # Strip any leading/trailing white space from data read.
#             row = [item.strip() for item in row]
#             yield row


def populate(repo: AbstractRepository):
    # # Load articles and tags into the repository.
    # load_articles_and_tags(data_path, repo)
    #
    # # Load users into the repository.
    # users = load_users(data_path, repo)
    #
    # # Load comments into the repository.
    # load_comments(data_path, repo, users)
    dir_name = os.path.dirname(os.path.abspath(__file__))
    games_file_name = os.path.join(dir_name, "data/games.csv")
    reader = GameFileCSVReader(games_file_name)
    reader.read_csv_file()
    games = reader.dataset_of_games

    for game in games:
        repo.add_game(game)

