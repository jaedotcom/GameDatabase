import csv
from pathlib import Path
from datetime import date, datetime
from typing import List

from games.adapters.repository import AbstractRepository

#need to add more

from games.domainmodel import Game, Genre, User, Publisher, Review, Wishlist

class MemoryRepository(Repository):
    # Articles ordered by date, not id. id is assumed unique.

    def __init__(self):
        self.__games = list()
        self.__games_index = dict()
        self.__tags = list()
        self.__users = list()
        self.__reviews = list()

    def add_game(self, game: Game):
        self.__games.append(game)


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def populate(data_path: Path, repo: memoryRepository):
    # Load articles and tags into the repository.
    load_articles_and_tags(data_path, repo)

    # Load users into the repository.
    users = load_users(data_path, repo)

    # Load comments into the repository.
    load_comments(data_path, repo, users)
