from pathlib import Path

from games.adapters.repository import AbstractRepository
from games.adapters import memoryRepository
from games.adapters.datareader import csv_db_reader


def populate(data_path: Path, repo: AbstractRepository, database_mode: bool):
    if database_mode:
        #load data through database methods
        pass


    pass