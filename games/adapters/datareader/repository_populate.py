from pathlib import Path
import os
from games.adapters.repository import AbstractRepository
from games.adapters import memoryRepository
from games.adapters.datareader.csvdatareader import GameFileCSVReader


def populate(data_path: str, repo: AbstractRepository):
    # dir_name = os.path.dirname(os.path.abspath(__file__))
    # games_file_name = os.path.join(dir_name, "data/games.csv")
    games_file_name = os.path.join(data_path, "games.csv")
    reader = GameFileCSVReader(games_file_name)
    reader.read_csv_file()
    games = reader.dataset_of_games
    genres = reader.dataset_of_genres

    for game in games:
        repo.add_game(game)

    for genre in genres:
        repo.add_genre(genre)