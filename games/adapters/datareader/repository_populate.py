from pathlib import Path

from games.adapters.repository import AbstractRepository
from games.adapters import memoryRepository
from games.adapters.datareader import csv_db_reader
from games.adapters.datareader.csvdatareader import GameFileCSVReader


def populate(data_path: Path, repo: AbstractRepository, database_mode: bool):
    if database_mode:
        #load data through database methods

        #we need to read the csv file
        # memoryRepository.populate(data_path, repo)
        pass


    pass