from pathlib import Path

from games.adapters.repository import AbstractRepository
#from games.adapters.csv_data_importer import load_users, load_games, load_reviews
from games.adapters.datareader.csvdatareader import


def populate(data_path: Path, repo: AbstractRepository, database_mode: bool):
    # load_users(data_path, repo)
    # games = load_games(data_path, repo)
    # load_reviews(reviews, data_path, repo)

    #load games
    #load publishers
    #load genres

    pass